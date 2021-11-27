import random
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def swap(array, i, j):
    array[i], array[j] = array[j], array[i]


def bubble_sort(array):
    swapped = True
    for i in range(len(array) - 1):
        if not swapped:
            break
        swapped = False
        for j in range(len(array) - 1 - i):
            if array[j] > array[j + 1]:
                swap(array, j, j + 1)
                swapped = True
            yield array  # возвращаем генератор


def insertion_sort(array):
    for i in range(1, len(array)):
        j = i
        while j > 0 and array[j] < array[j - 1]:
            swap(array, j, j - 1)
            j -= 1
            yield array


def merge(array, start, mid, end):
    merged = []
    left = start
    right = mid + 1
    while left <= mid and right <= end:
        if array[left] < array[right]:
            merged.append(array[left])
            left += 1
        else:
            merged.append(array[right])
            right += 1
    while left <= mid:
        merged.append(array[left])
        left += 1
    while right <= end:
        merged.append(array[right])
        right += 1
    for i, sorted_val in enumerate(merged):  # индекс элемента и его значение
        array[start + i] = sorted_val
        yield array


def merge_sort(array, start, end):
    if end <= start:
        return
    mid = start + ((end - start + 1) // 2) - 1
    yield from merge_sort(array, start, mid)
    yield from merge_sort(array, mid + 1, end)
    yield from merge(array, start, mid, end)
    yield array


def quick_sort(array, start, end):
    if start >= end:
        return
    pivot = array[end]
    pivot_index = start
    for i in range(start, end):
        if array[i] < pivot:
            swap(array, i, pivot_index)
            pivot_index += 1
        yield array
    swap(array, end, pivot_index)
    yield array
    yield from quick_sort(array, start, pivot_index - 1)
    yield from quick_sort(array, pivot_index + 1, end)


def selection_sort(array):
    for i in range(len(array)):
        min_value = array[i]
        min_index = i
        for j in range(i, len(array)):
            if array[j] < min_value:
                min_value = array[j]
                min_index = j
            yield array
        swap(array, i, min_index)
        yield array


if __name__ == "__main__":
    N = int(input("Введите размер массива: "))
    method_msg = "Выберите сортировку:\n(b)ubble\n(i)nsertion\n(m)erge \
        \n(q)uick\n(s)election\n"
    method = input(method_msg)

    A = [x + 1 for x in range(N)]  # рандомный массив с рандомными числами
    random.seed(time.time())
    random.shuffle(A)

    # Достаем генратор из сортировок
    if method == "b":
        title = "Bubble sort"
        generator = bubble_sort(A)
    elif method == "i":
        title = "Insertion sort"
        generator = insertion_sort(A)
    elif method == "m":
        title = "Merge sort"
        generator = merge_sort(A, 0, N - 1)
    elif method == "q":
        title = "Quicksort"
        generator = quick_sort(A, 0, N - 1)
    else:
        title = "Selection sort"
        generator = selection_sort(A)

    fig, ax = plt.subplots()
    ax.set_title(title)
    bar_rects = ax.bar(range(len(A)), A, align="edge")
    ax.set_xlim(0, N)
    ax.set_ylim(0, int(1.07 * N))
    text = ax.text(0.02, 0.95, "", transform=ax.transAxes)
    iteration = [0]


    def update_fig(array, rects, iteration):
        for rect, val in zip(rects, array):
            rect.set_height(val)
        iteration[0] += 1
        text.set_text(f"№ операции: {format(iteration[0])}")

    anim = animation.FuncAnimation(fig, func=update_fig,
        fargs=(bar_rects, iteration), frames=generator, interval=1,
        repeat=False)
    plt.show()
