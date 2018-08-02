from pandas import read_csv
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler

def Create_score_model(X_test):
    df = read_csv('df.csv', encoding='utf-8')
    Y = df['imdb_score'].values.reshape(-1, 1)
    df = df.drop(['imdb_score', 'gross'], axis=1)
    X = df
 #   X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=7)
    pipe_GBR = Pipeline([('sc', StandardScaler()),
                         ('GBR', GradientBoostingRegressor(n_estimators=200))])
    pipe_GBR.fit(X, Y.ravel())
    return pipe_GBR.predict(X_test)

def Create_gross_model(x_test):
    df = read_csv('df.csv', encoding='utf-8')
    sc = StandardScaler()
    Y = sc.fit_transform(df['gross'].values.reshape(-1, 1))
    df = df.drop(['imdb_score', 'gross'], axis=1)
    X = df
   # X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=7)
    pipe_GBR = Pipeline([('ssc', StandardScaler()),
                         ('GBR', GradientBoostingRegressor(n_estimators=100))])
    pipe_GBR.fit(X, Y.ravel())
    pre = pipe_GBR.predict(x_test)
    return sc.inverse_transform(pre)






