# load model
import pickle
filename='QDA.sav'
test_cases = [[100,20,36.6]]
loaded_model = pickle.load(open(filename, 'rb'))
result = loaded_model.predict(test_cases)
print(result)