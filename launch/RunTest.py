from behave.__main__ import main as behave_main


# To Debug & execute a feature file, within IntelliJ IDE
behave_main("../features/Login.feature")

# To Debug & execute Feature file with a tag, from IntelliJ IDE
# behave_main("-t @test-2 ../features/Login.feature")