import pickle
from sklearn.externals import joblib

#joblib.load()
data = joblib.load("emo_analysis.pkl")

print data