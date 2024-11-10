class OuterClass:
    def __init__(self, value):
        self.outer_value = value
        self.inner_instance = self.InnerClass(self)

    def display_outer_value(self):
        print(f"Outer value is: {self.outer_value}")

    class InnerClass:
        def __init__(self, outer_instance):
            self.outer_instance = outer_instance

        def access_outer(self):
            print(f"Accessing outer value: {self.outer_instance.outer_value}")
            self.outer_instance.display_outer_value()

# Usage
outer = OuterClass(42)
outer.inner_instance.access_outer()

# Alter the outer_value
outer.outer_value = 99
outer.inner_instance.access_outer()