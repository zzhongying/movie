from pandas import read_csv,DataFrame
from sklearn.pipeline import Pipeline
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler

def Create_score_model(x_test):
    result = []
    x_test.extend(Type_conversion(x_test.pop(-1)))
    x_test=DataFrame(x_test).T
    df = read_csv('data.csv', encoding='utf-8')
    sc = StandardScaler()
    Y2 = sc.fit_transform(df['Box_office'].values.reshape(-1, 1))
    Y1 = df['IMDB'].values.reshape(-1, 1)
    df = df.drop(['IMDB', 'Box_office'], axis=1)
    X = df
    pipe_GBR = Pipeline([('sc', StandardScaler()),
                         ('GBR', GradientBoostingRegressor(n_estimators=200))])
    pipe_GBR.fit(X, Y1.ravel())
    result.append(pipe_GBR.predict(x_test)[0])
    pipe_GBR = Pipeline([('ssc', StandardScaler()),
                         ('GBR', GradientBoostingRegressor(n_estimators=100))])
    pipe_GBR.fit(X, Y2.ravel())
    pre = pipe_GBR.predict(x_test)
    result.append(sc.inverse_transform(pre)[0])
    return result


# def Create_gross_model(x_test):
#     x_test.extend(Type_conversion(x_test.pop(-1)))
#     x_test=DataFrame(x_test).T
#     df = read_csv('data.csv', encoding='utf-8')
#     sc = StandardScaler()
#     Y = sc.fit_transform(df['Box_office'].values.reshape(-1, 1))
#     df = df.drop(['IMDB', 'Box_office'], axis=1)
#     X = df
#     pipe_GBR = Pipeline([('ssc', StandardScaler()),
#                          ('GBR', GradientBoostingRegressor(n_estimators=100))])
#     pipe_GBR.fit(X, Y.ravel())
#     pre = pipe_GBR.predict(x_test)
#     return sc.inverse_transform(pre)

def Type_conversion(test):
    genres = ['Action',
              'Adventure',
              'Comedy',
              'Crime',
              'Documentary',
              'Drama',
              'Family',
              'Fantasy',
              'Horror',
              'Music',
              'Mystery',
              'Romance',
              'Sci-Fi',
              'Thriller',
              'War',
              'Western']

    return list(map(lambda x:1 if x in test else 0,genres))


if __name__ == '__main__':
    dd = [25000000,0,142,108000,'Crime|Drama']
    #print(Create_gross_model(cc))
    print(Create_score_model(dd))




