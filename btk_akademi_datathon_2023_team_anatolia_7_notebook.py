# -*- coding: utf-8 -*-
"""BTK Akademi Datathon 2023 Team-Anatolia-7 Notebook

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YOD43JVc-RzD3An-l8uN00KPEjbeYz4X
"""

import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV

train_data = pd.read_csv("train.csv", encoding="utf-8")
test_data = pd.read_csv("test_x.csv", encoding="utf-8")

columns_to_drop = ["index"]
train_data = train_data.drop(columns=columns_to_drop)

categorical_columns = ["Cinsiyet", "Yaş Grubu", "Medeni Durum", "Eğitim Düzeyi",
                       "İstihdam Durumu", "Yaşadığı Şehir", "En Çok İlgilendiği Ürün Grubu",
                       "Eğitime Devam Etme Durumu"]
label_encoders = {}
for col in categorical_columns:
    le = LabelEncoder()
    train_data[col] = le.fit_transform(train_data[col])
    test_data[col] = le.transform(test_data[col])
    label_encoders[col] = le

X = train_data.drop(columns=["Öbek İsmi"])
y = train_data["Öbek İsmi"]

X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=0.2, random_state=42)

param_grid = {
    'n_estimators': [50, 100, 150],
    'max_depth': [None, 10, 20],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

grid_search = GridSearchCV(estimator=RandomForestClassifier(random_state=42),
                           param_grid=param_grid,
                           scoring='accuracy',
                           cv=3)
grid_search.fit(X_train, y_train)

print("En iyi parametreler:", grid_search.best_params_)
print("En iyi doğruluk:", grid_search.best_score_)

best_params = grid_search.best_params_
model = RandomForestClassifier(n_estimators=best_params['n_estimators'],
                               max_depth=best_params['max_depth'],
                               min_samples_split=best_params['min_samples_split'],
                               min_samples_leaf=best_params['min_samples_leaf'],
                               random_state=42)

model.fit(X_train, y_train)

valid_predictions = model.predict(X_valid)

accuracy = accuracy_score(y_valid, valid_predictions)
print("Doğruluk:", accuracy)

feature_columns = X.columns.tolist()

test_data = test_data[feature_columns]

test_predictions = model.predict(test_data)

submission = pd.DataFrame({"id": range(len(test_predictions)), "Öbek İsmi": test_predictions})

submission.to_csv("submission.csv", index=False)

import pandas as pd
from sklearn.preprocessing import LabelEncoder, RobustScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.feature_selection import SelectFromModel

train_data = pd.read_csv("train.csv", encoding="utf-8")
test_data = pd.read_csv("test_x.csv", encoding="utf-8")

columns_to_drop = ["index"]
train_data = train_data.drop(columns=columns_to_drop)

categorical_columns = ["Cinsiyet", "Yaş Grubu", "Medeni Durum", "Eğitim Düzeyi",
                       "İstihdam Durumu", "Yaşadığı Şehir", "En Çok İlgilendiği Ürün Grubu",
                       "Eğitime Devam Etme Durumu"]
label_encoders = {}
for col in categorical_columns:
    le = LabelEncoder()
    train_data[col] = le.fit_transform(train_data[col])
    test_data[col] = le.transform(test_data[col])
    label_encoders[col] = le

for col in categorical_columns:
    class_distribution = pd.crosstab(index=train_data[col].apply(lambda x: label_encoders[col].inverse_transform([x])[0]), columns="count")
    print(f"Sınıf Dağılımı - {col}:\n{class_distribution}\n")

X = train_data.drop(columns=["Öbek İsmi"])
y = train_data["Öbek İsmi"]

scaler = RobustScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_valid, y_train, y_valid = train_test_split(X_scaled, y, test_size=0.2, random_state=42, shuffle=True)

model = RandomForestClassifier(n_estimators=200, max_depth=15, min_samples_split=5, random_state=42)
model.fit(X_train, y_train)

feature_importances = model.feature_importances_
selector = SelectFromModel(estimator=model, threshold=0.005)
selector.fit(X_train, y_train)
important_feature_indices = selector.get_support(indices=True)

X_train_selected = X_train[:, important_feature_indices]
X_valid_selected = X_valid[:, important_feature_indices]
test_data_selected = scaler.transform(test_data.values[:, important_feature_indices])

model_selected = RandomForestClassifier(n_estimators=200, max_depth=15, min_samples_split=5, random_state=42)
model_selected.fit(X_train_selected, y_train)

valid_predictions = model_selected.predict(X_valid_selected)

accuracy = accuracy_score(y_valid, valid_predictions)
print("Doğruluk:", accuracy)

test_predictions = model_selected.predict(test_data_selected)

submission = pd.DataFrame({"id": range(len(test_predictions)), "Öbek İsmi": test_predictions})

submission.to_csv("submission.csv", index=False)

import pandas as pd
from sklearn.preprocessing import LabelEncoder
import seaborn as sns
import matplotlib.pyplot as plt


train_data = pd.read_csv("train.csv", encoding="utf-8")
test_data = pd.read_csv("test_x.csv", encoding="utf-8")


columns_to_drop = ["index"]
train_data = train_data.drop(columns=columns_to_drop)
test_data = test_data.drop(columns=columns_to_drop)

all_data = pd.concat([train_data, test_data])

categorical_columns = ["Cinsiyet", "Yaş Grubu", "Medeni Durum", "Eğitim Düzeyi",
                       "İstihdam Durumu", "Yaşadığı Şehir", "En Çok İlgilendiği Ürün Grubu",
                       "Eğitime Devam Etme Durumu"]
label_encoders = {}
for col in categorical_columns:
    le = LabelEncoder()
    all_data[col] = le.fit_transform(all_data[col])
    label_encoders[col] = le

class_column = "Öbek İsmi"
classes = all_data[class_column].unique()

for col in all_data.columns:
    if col != class_column:
        plt.figure(figsize=(10, 8))
        ax = sns.countplot(data=all_data, x=col, hue=class_column, palette="Set2")
        plt.title(f"{col} Sınıfına Göre Öbek Dağılımı")
        plt.xlabel(col)
        plt.ylabel("Sayı")
        plt.xticks(rotation=45)
        plt.legend(title=class_column, labels=classes)

        le = label_encoders.get(col)
        if le:
            ax.set_xticklabels(le.inverse_transform(range(len(ax.get_xticks()))))

        plt.show()

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, RobustScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import GridSearchCV
from sklearn.utils import resample
from sklearn.pipeline import Pipeline

train_data = pd.read_csv("train.csv", encoding="utf-8")
test_data = pd.read_csv("test_x.csv", encoding="utf-8")

columns_to_drop = ["index"]
train_data = train_data.drop(columns=columns_to_drop)
test_data = test_data.drop(columns=columns_to_drop)

X = train_data.drop(columns=["Öbek İsmi"])
y = train_data["Öbek İsmi"]

X_upsampled, y_upsampled = resample(X[y == "obek_6"], y[y == "obek_6"],
                                    n_samples=X[y != "obek_6"].shape[0], random_state=42)
X_balanced = pd.concat([X[y != "obek_6"], X_upsampled])
y_balanced = pd.concat([y[y != "obek_6"], y_upsampled])

categorical_columns = ["Cinsiyet", "Yaş Grubu", "Medeni Durum", "Eğitim Düzeyi",
                       "İstihdam Durumu", "Yaşadığı Şehir", "En Çok İlgilendiği Ürün Grubu",
                       "Eğitime Devam Etme Durumu"]
encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)
X_encoded = encoder.fit_transform(X_balanced[categorical_columns])
encoded_columns = encoder.get_feature_names_out(input_features=categorical_columns)
X_encoded_df = pd.DataFrame(X_encoded, columns=encoded_columns, index=X_balanced.index)

X_balanced = pd.concat([X_balanced.drop(columns=categorical_columns), X_encoded_df], axis=1)

scaler = RobustScaler()
X_scaled = scaler.fit_transform(X_balanced)

X_train, X_valid, y_train, y_valid = train_test_split(X_scaled, y_balanced, test_size=0.2, random_state=42, shuffle=True)

pipeline = Pipeline([
    ('model', RandomForestClassifier(class_weight='balanced', random_state=42))
])

param_grid = {
    'model__n_estimators': [100, 200],
    'model__max_depth': [10, 20]
}

grid_search = GridSearchCV(pipeline, param_grid, cv=3, scoring='accuracy')
grid_search.fit(X_train, y_train)

best_model = grid_search.best_estimator_

valid_predictions = best_model.predict(X_valid)

accuracy = accuracy_score(y_valid, valid_predictions)
print("Doğruluk:", accuracy)
print(classification_report(y_valid, valid_predictions))

test_encoded = encoder.transform(test_data[categorical_columns])
test_encoded_df = pd.DataFrame(test_encoded, columns=encoded_columns, index=test_data.index)
test_data_processed = pd.concat([test_data.drop(columns=categorical_columns), test_encoded_df], axis=1)
test_data_scaled = scaler.transform(test_data_processed)
test_predictions = best_model.predict(test_data_scaled)

submission = pd.DataFrame({"id": range(len(test_predictions)), "Öbek İsmi": test_predictions})

try:
    submission.to_csv("submission.csv", index=False)
except Exception as e:
    print("Dosya kaydetme hatası:", e)