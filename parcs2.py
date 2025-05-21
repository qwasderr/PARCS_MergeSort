from Pyro4 import expose

class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers

    def solve(self):
        arr = self.read_input()
        chunk_size = len(arr) / len(self.workers)
        mapped = []
        for i in xrange(len(self.workers)):
            start = int(i * chunk_size)
            end = int((i + 1) * chunk_size) if i != len(self.workers) - 1 else len(arr)
            chunk = arr[start:end]
            mapped.append(self.workers[i].mymap(chunk))
        result = self.myreduce(mapped)
        self.write_output(result)

    @staticmethod
    @expose
    def mymap(subarray):
        return sorted(subarray)

    @staticmethod
    @expose
    def myreduce(mapped):
        sorted_lists = [m.value for m in mapped]

        def merge(left, right):
            merged = []
            i = j = 0
            while i < len(left) and j < len(right):
                if left[i] < right[j]:
                    merged.append(left[i])
                    i += 1
                else:
                    merged.append(right[j])
                    j += 1
            merged.extend(left[i:])
            merged.extend(right[j:])
            return merged

        while len(sorted_lists) > 1:
            temp = []
            for i in xrange(0, len(sorted_lists), 2):
                if i + 1 < len(sorted_lists):
                    merged = merge(sorted_lists[i], sorted_lists[i+1])
                else:
                    merged = sorted_lists[i]
                temp.append(merged)
            sorted_lists = temp

        return sorted_lists[0]

    def read_input(self):
        f = open(self.input_file_name, 'r')
        arr = map(int, f.readline().split())
        f.close()
        return arr

    def write_output(self, output):
        f = open(self.output_file_name, 'w')
        f.write(' '.join(map(str, output)) + '\n')
        f.close()
