from behave.__main__ import main as behave_main


# To Debug & execute a feature file, within IntelliJ IDE
# behave_main("../features/CheckoutThis.feature")

# To Debug & execute Feature file with a tag, from IntelliJ IDE
behave_main("-t @final ../features/final/par_OrangeHRM_.feature")