import numpy as np

from sklearn.cross_validation import train_test_split
import os
import shutil

path = 'E:\\Scholastic\\NITK//Year_3_NITK\\Sem-5//Audio Signal Processing\\Data\\visual\\'
dest_path = 'E:\\Scholastic\\NITK//Year_3_NITK\\Sem-5//Audio Signal Processing\\Data\\visual_train\\'
dest_path2 = 'E:\\Scholastic\\NITK//Year_3_NITK\\Sem-5//Audio Signal Processing\\Data\\visual_test\\'
X = y = os.listdir(path)


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

for file in X_train:
    newname = dest_path+file
    shutil.copyfile(path+file,newname)
    
for file in X_test:
    oldname = path+file
    newname = dest_path2+file
    shutil.copyfile(oldname,newname)