import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report
from xgboost import XGBClassifier
from imblearn.over_sampling import SMOTE


users = pd.read_csv("https://s3.amazonaws.com/asana-data-interview/takehome_users-intern.csv")
user_engagement = pd.read_csv("https://s3.amazonaws.com/asana-data-interview/takehome_user_engagement-intern.csv")
# Convert the 'time_stamp' in user_engagement to datetime format
user_engagement['time_stamp'] = pd.to_datetime(user_engagement['time_stamp'])

# Extract the date (without time) for easier comparison
user_engagement['date'] = user_engagement['time_stamp'].dt.date

# Sort by user_id and date
user_engagement = user_engagement.sort_values(['user_id', 'date'])

# Group by user_id and apply a custom function to find adopted users
def is_adopted(dates):
    unique_dates = set()
    for i in range(len(dates)):
        start_date = dates[i]
        within_window = {start_date}
        for j in range(i + 1, len(dates)):
            if (dates[j] - start_date).days <= 7:
                within_window.add(dates[j])
            else:
                break
        if len(within_window) >= 3:
            return True
    return False


adopted_users = user_engagement.groupby('user_id')['date'].apply(lambda x: is_adopted(list(x))).reset_index()

adopted_users = adopted_users[adopted_users['date'] == True]['user_id'].unique()

users['adopted_user'] = users['object_id'].isin(adopted_users)


total_users = len(users)


total_adopted_users = users['adopted_user'].sum()


adoption_rate = total_adopted_users / total_users * 100


print(f"Adoption Rate: {adoption_rate:.2f}%")


data = {'Status': ['Adopted', 'Not Adopted'],
        'Count': [total_adopted_users, total_users - total_adopted_users]}
adoption_df = pd.DataFrame(data)

sns.barplot(x='Status', y='Count', data=adoption_df)
plt.title('General Adoption Rate')
plt.ylabel('Number of Users')
plt.xlabel('User Status')
plt.show()



plt.figure(figsize=(10, 6))
sns.countplot(data=users, x='creation_source', hue='adopted_user')
plt.title('Adoption Status by Creation Source')
plt.xlabel('Creation Source')
plt.ylabel('Number of Users')
plt.xticks(rotation=45)
plt.show()


plt.figure(figsize=(6, 4))
sns.countplot(data=users, x='opted_in_to_mailing_list', hue='adopted_user')
plt.title('Adoption Status by Opted-in to Mailing List')
plt.xlabel('Opted-in to Mailing List')
plt.ylabel('Number of Users')
plt.show()


plt.figure(figsize=(6, 4))
sns.countplot(data=users, x='enabled_for_marketing_drip', hue='adopted_user')
plt.title('Adoption Status by Enabled for Marketing Drip')
plt.xlabel('Enabled for Marketing Drip')
plt.ylabel('Number of Users')
plt.show()


users_numeric = users.select_dtypes(include=['number', 'bool'])




X = users[['creation_source', 'opted_in_to_mailing_list', 'enabled_for_marketing_drip', 'org_id']]
y = users['adopted_user'].astype(int)
X = pd.get_dummies(X, drop_first=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
smote = SMOTE(random_state=42)
X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)
xgb_model = XGBClassifier(eval_metric='logloss', random_state=42)
xgb_model.fit(X_train_smote, y_train_smote)


y_pred = xgb_model.predict(X_test)
print(classification_report(y_test, y_pred))


importances = pd.Series(xgb_model.feature_importances_, index=X.columns)
importances.sort_values().plot(kind='barh', title='Feature Importance')
plt.show()


