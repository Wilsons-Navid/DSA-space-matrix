class InvalidArgumentError(Exception):
    """Custom exception for invalid input format."""
    pass

class SparseMatrix:
    def __init__(self, matrixFilePath=None, numRows=None, numCols=None):
        if matrixFilePath:
            self.num_rows, self.num_cols, self.data = self._load_from_file(matrixFilePath)
        else:
            self.num_rows = numRows
            self.num_cols = numCols
            self.data = {}

    def _load_from_file(self, file_path):
        data = {}
        try:
            with open(file_path, 'r') as f:
                num_rows = int(f.readline().split('=')[1].strip())
                num_cols = int(f.readline().split('=')[1].strip())
                for line in f:
                    line = line.strip()
                    if line:  # Ignore empty lines
                        if not line.startswith('(') or not line.endswith(')'):
                            raise InvalidArgumentError("Input file has wrong format")
                        try:
                            row, col, value = map(int, line.strip('()').split(','))
                        except ValueError:
                            raise InvalidArgumentError("Input file has wrong format")
                        if value != 0:
                            data[(row, col)] = value
            return num_rows, num_cols, data
        except Exception:
            raise InvalidArgumentError("Input file has wrong format")

    def getElement(self, currRow, currCol):
        return self.data.get((currRow, currCol), 0)

    def setElement(self, currRow, currCol, value):
        if value != 0:
            self.data[(currRow, currCol)] = value
        elif (currRow, currCol) in self.data:
            del self.data[(currRow, currCol)]

    def add(self, other):
        if self.num_rows != other.num_rows or self.num_cols != other.num_cols:
            raise InvalidArgumentError("Matrix dimensions must be the same for addition.")
        result = SparseMatrix(numRows=self.num_rows, numCols=self.num_cols)
        result.data = self.data.copy()
        for (r, c), v in other.data.items():
            result.setElement(r, c, result.getElement(r, c) + v)
        return result

    def subtract(self, other):
        if self.num_rows != other.num_rows or self.num_cols != other.num_cols:
            raise InvalidArgumentError("Matrix dimensions must be the same for subtraction.")
        result = SparseMatrix(numRows=self.num_rows, numCols=self.num_cols)
        result.data = self.data.copy()
        for (r, c), v in other.data.items():
            result.setElement(r, c, result.getElement(r, c) - v)
        return result

    def multiply(self, other):
        if self.num_cols != other.num_rows:
            raise InvalidArgumentError("Matrix dimensions do not allow multiplication.")
        result = SparseMatrix(numRows=self.num_rows, numCols=other.num_cols)
        for (r1, c1), v1 in self.data.items():
            for c2 in range(other.num_cols):
                v2 = other.getElement(c1, c2)
                if v2 != 0:
                    result.setElement(r1, c2, result.getElement(r1, c2) + v1 * v2)
        return result

    def __str__(self):
        elements = [f"({r}, {c}, {v})" for (r, c), v in sorted(self.data.items())]
        return f"SparseMatrix({self.num_rows}, {self.num_cols}): " + ", ".join(elements)

def main():
    try:
        # User selects operation
        operation = input("Select operation (add, subtract, multiply): ").strip().lower()
        file1 = input("Enter the path to the first matrix file: ").strip()
        file2 = input("Enter the path to the second matrix file: ").strip()

        # Load matrices
        matrix1 = SparseMatrix(matrixFilePath=file1)
        matrix2 = SparseMatrix(matrixFilePath=file2)

        # Perform selected operation
        if operation == "add":
            result = matrix1.add(matrix2)
        elif operation == "subtract":
            result = matrix1.subtract(matrix2)
        elif operation == "multiply":
            result = matrix1.multiply(matrix2)
        else:
            raise InvalidArgumentError("Invalid operation selected.")

        # Display result
        print("Result:")
        print(result)

    except InvalidArgumentError as e:
        print(e)
    except FileNotFoundError:
        print("The specified file was not found.")

if __name__ == "__main__":
    main()