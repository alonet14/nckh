# load model
import pickle
filename='QDA.sav'
test_data = [[70, 20, 37]]
loaded_model = pickle.load(open(filename, 'rb'))
result = loaded_model.predict(test_data)
print(result)