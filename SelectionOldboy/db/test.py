import pickle
with open('student_classroom','rb') as f:
    data=pickle.load(f)

print(data)