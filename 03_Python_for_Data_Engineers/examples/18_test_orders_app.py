"""Runs 18_orders_app.py headlessly with Streamlit's AppTest and prints what it renders."""
from streamlit.testing.v1 import AppTest

at = AppTest.from_file("18_orders_app.py", default_timeout=60).run()
assert not at.exception


def show(label):
    metrics = ", ".join(f"{m.label}={m.value}" for m in at.metric)
    print(f"{label:<45} {metrics}")


print("Title:", at.title[0].value)
show("Default view (completed orders, all regions)")
at.sidebar.checkbox[0].uncheck().run()
show("Untick 'Completed orders only'")
at.sidebar.multiselect[0].set_value(["West"]).run()
show("Region = West, all statuses")
at.sidebar.multiselect[0].set_value([]).run()
print("No region selected ->", at.warning[0].value)
