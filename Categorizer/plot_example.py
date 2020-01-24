import matplotlib.pyplot as plt

from Rignak_Misc.plt import imshow

LIMIT = 8


def plot_example(example, prediction, labels, limit=LIMIT, denormalizer=None):
    input_, truth = example
    input_ = input_[:limit]
    n = input_.shape[0]
    plt.figure(figsize=(18, 8))
    plt.tight_layout()
    for i, (im, classes) in enumerate(zip(input_, prediction)):
        print('plot_example.py', denormalizer)
        if i != 0:
            tick_label = [' ' for _ in labels]
        else:
            tick_label = labels
        plt.subplot(2, n, i + 1)
        imshow(im, denormalizer=denormalizer)

        plt.subplot(2, n, i + 1 + n)
        plt.barh(labels, truth[i], tick_label=tick_label, color='C1')
        plt.barh(labels, classes, tick_label=tick_label, color='C0')
        plt.xlim(0, 1)
        plt.yticks()
    plt.tight_layout()
