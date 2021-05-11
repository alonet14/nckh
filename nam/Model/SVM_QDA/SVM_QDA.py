import csv
import pickle

import numpy as np
import pandas as pd
from sklearn import metrics
import matplotlib.pyplot as plt
from matplotlib import colors
from sklearn import svm
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis as QDA
from sklearn.linear_model import LogisticRegression
import time
from sklearn.model_selection import train_test_split

# load data
def load_data(file_path):
    dataset = pd.read_csv(file_path)
    dataset = dataset.iloc[:, [0, 1, 2]].values
    return dataset


def cross_validation(clf, X, Y):
    from sklearn.model_selection import learning_curve, validation_curve, cross_validate, KFold
    scorings = ['precision_weighted', 'recall_weighted', 'f1_weighted', 'accuracy']

    keys = ['train_accuracy', 'test_precision_weighted', 'test_recall_weighted', 'test_f1_weighted']

    results = []
    for i in range(10):  # since we shuffle KFold, we should do a lot of times and get the average results
        kfold = KFold(n_splits=4, shuffle=True)

        scores = cross_validate(clf, X, Y, scoring=scorings, cv=kfold, return_train_score=True)
        results_i = []  # all scores at i-th iteration
        for key in keys:
            results_i.append(np.mean(scores[key]))

        results.append(results_i)
    results = np.array(results)

    avg_results = np.mean(results, axis=0)

    ## print average scores:
    for score, key in zip(avg_results, keys):
        print("{}: {:.5f}".format(key, score))

    return avg_results


def make_meshgrid(x, y, h=.02):
    x_min, x_max = x.min() - 1, x.max() + 1
    y_min, y_max = y.min() - 1, y.max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))
    return xx, yy

# Vẽ đồ thị
def plot(models, title, healthy, infected, healthy_labels, infected_labels):
    from mpl_toolkits.mplot3d import Axes3D

    fig = plt.figure(figsize=(16, 10))

    ax1 = fig.add_subplot(231)
    ax2 = fig.add_subplot(232)
    ax3 = fig.add_subplot(233)
    ax4 = fig.add_subplot(223, projection='3d')

    SPACE_SAMPLING_POINTS = 500

    axes = [ax1, ax2, ax3]
    X = np.vstack((healthy, infected))
    Y = np.hstack((healthy_labels, infected_labels))

    # Plot data points
    ax1.scatter(healthy[:, 0], healthy[:, 1], c='b', marker='v', label='Healthy', s=15)
    ax1.scatter(infected[:, 0], infected[:, 1], c='r', label='Infected', s=15)
    ax2.scatter(healthy[:, 1], healthy[:, 2], c='b', marker='v', label='Healthy', s=15)
    ax2.scatter(infected[:, 1], infected[:, 2], c='r', label='Infected', s=15)
    ax3.scatter(healthy[:, 2], healthy[:, 0], c='b', marker='v', label='Healthy', s=15)
    ax3.scatter(infected[:, 2], infected[:, 0], c='r', label='Infected', s=15)
    ax4.scatter(healthy[:, 0], healthy[:, 1], healthy[:, 2], c='b', marker='v', label='Healthy', s=15)
    ax4.scatter(infected[:, 0], infected[:, 1], infected[:, 2], c='r', label='Infected', s=15)

    # Plot decision boundaries of all models
    features = [[0, 1], [1, 2], [2, 0]]
    for clf, name in zip(models, title):
        if name == 'SVM':
            # 2d Plot
            for ax, feat in zip(axes, features):
                clf.fit(np.c_[X[:, feat[0]], X[:, feat[1]]], Y)

                if ax == ax1:
                    xx = np.linspace(50, 120, 10)
                elif ax == ax2:
                    xx = np.linspace(5, 50, 2)
                elif ax == ax3:
                    xx = np.linspace(35, 42, 2)
                y_ = lambda x: (-clf.intercept_[0] - clf.coef_[0][0] * x) / clf.coef_[0][1]

                ax.plot(xx, y_(xx), color='purple', linewidth=1.5, ls='--')
            # 3d plot
            clf.fit(X, Y)

            z = lambda x, y: (-clf.intercept_[0] - clf.coef_[0][0] * x - clf.coef_[0][1] * y) / clf.coef_[0][2]
            #
            SPACE_SAMPLING_POINTS = 100
            X_MIN = 83
            X_MAX = 103
            Y_MIN = 0
            Y_MAX = 0.3

            # Generate a regular grid to sample the 3D space for various operations later
            x, y = np.meshgrid(np.linspace(X_MIN, X_MAX, SPACE_SAMPLING_POINTS),
                               np.linspace(Y_MIN, Y_MAX, SPACE_SAMPLING_POINTS))
            # Plot surface.
            ax4.plot_surface(x, y, z(x, y), color='grey', antialiased=False)

    ax1.legend()
    ax2.legend()
    ax3.legend()
    ax4.legend()
    ax1.set_xlabel("HR [bpm]", weight='bold')
    ax2.set_xlabel("RR [BPM]", weight='bold')
    ax3.set_xlabel("T [oC]", weight='bold')
    ax1.set_ylabel("RR [BPM]", weight='bold')
    ax3.set_ylabel("HR [bpm]", weight='bold')
    ax2.set_ylabel("T [oC]", weight='bold')
    ax4.set_xlabel("HR [bpm]", weight='bold')
    ax4.set_ylabel("RR [BPM]", weight='bold')
    ax4.set_zlabel("T [oC]", weight='bold')
    #
    plt.show()

def main():
    # input
    healthy = load_data("data/HR_RR_T_SVM_1.csv")
    infected = load_data("data/HR_RR_T_SVM.csv")

    # Training

    #### Training
    healthy_labels = np.ones(healthy.shape[0])  # Label: 1
    infected_labels = np.zeros(infected.shape[0])  # Label: 0

    X = np.vstack((healthy, infected))
    Y = np.hstack((healthy_labels, infected_labels))

    models = [svm.SVC(kernel='linear', C=5000),
              QDA()]

    names = ['SVM', 'QDA']

    #train and test
    test_cases = [[76,24.576,36.6]]

    for model, name in zip(models, names):
        print(name)
        cross_validation(model, X, Y)
        t1 = time.time()
        model.fit(X, Y)
        t2 = time.time()
        y_pred = model.predict(test_cases)
        print(y_pred)
        t3 = time.time()
        print("Training time: {:.2f}ms\nTest_time: {:.2f}ms".format(1000 * (t2 - t1), 1000 * (t3 - t2)))
        filename = f'{name}.sav'
        pickle.dump(model, open(filename, 'wb'))

    # Vẽ đồ thị
    plot(models, names, healthy, infected, healthy_labels, infected_labels)
    # save the model to disk

if __name__ == "__main__":
    main()


