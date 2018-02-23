
class CalculatorSample:
    def performmaths(self, choice, num1, num2):
        if (1 <= choice <= 3):
            if choice == 1:
                res = num1 + num2
                return res
            elif choice == 2:
                res = num1 - num2
                return res
            elif choice == 3:
                res = num1 * num2
                return res
            else:
                res = num1 / num2
                return res
        else:
            return "Wrong input..!!"
