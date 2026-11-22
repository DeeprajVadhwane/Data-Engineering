# Examples

Each topic has one Python file containing every runnable example from the document, in order. The output shown in the documents was captured by running this code.

| File | Topic | What it shows |
|---|---|---|
| `01_introduction_to_python_for_data_engineering.py` | [01](../01-introduction-to-python-for-data-engineering.md) | A first revenue-by-region script, syntax and data types |
| `02_literals_keywords_and_data_types.py` | [02](../02-literals-keywords-and-data-types.md) | Identifiers, keywords, variables, `print()`, `input()` |
| `03_operators_and_intro_conditions.py` | [03](../03-operators-and-intro-conditions.md) | All operator families, `==` versus `is` |
| `04_lists_and_intro_to_for_loops.py` | [04](../04-lists-and-intro-to-for-loops.md) | Lists, slicing, methods, loops, `enumerate` |
| `05_tuples_and_sets.py` | [05](../05-tuples-and-sets.md) | Tuples, sets, set operations |
| `06_dictionary.py` | [06](../06-dictionary.md) | Dictionaries, methods, copying |
| `07_strings_i.py` | [07](../07-strings-i.md) | Indexing, methods, formatting, type-casting |
| `08_conditional_statements.py` | [08](../08-conditional-statements.md) | `if`, `elif`, `else`, nesting |
| `09_while_loops.py` | [09](../09-while-loops.md) | `while`, `break`, `continue`, retry, patterns |
| `10_strings_ii.py` | [10](../10-strings-ii.md) | String problems with `chr` and `ord` |
| `11_for_else_while_else_and_comprehensions.py` | [11](../11-for-else-while-else-and-comprehensions.md) | Loop `else`, comprehensions |
| `12_functions_i.py` | [12](../12-functions-i.md) | Defining and calling functions |
| `13_functions_ii.py` | [13](../13-functions-ii.md) | Lambda, `map`, `filter`, `reduce`, scope |
| `14_oop_classes_and_objects.py` | [14](../14-oop-classes-and-objects.md) | Classes, objects, constructors |
| `15_oop_inheritance_and_abstraction.py` | [15](../15-oop-inheritance-and-abstraction.md) | Inheritance kinds, MRO, abstract classes |
| `16_oop_polymorphism_and_encapsulation.py` | [16](../16-oop-polymorphism-and-encapsulation.md) | Duck typing, overriding, `property` |
| `17_file_handling_and_exception_handling.py` | [17](../17-file-handling-and-exception-handling.md) | Files, CSV, JSON, exceptions |
| `17_robust_file_pipeline.py` | [17](../17-file-handling-and-exception-handling.md) | A complete pipeline with rejects, retries and logging |
| `18_orders_app.py` | [18](../18-streamlit.md) | The Streamlit orders app |
| `18_test_orders_app.py` | [18](../18-streamlit.md) | Headless test of the app with `AppTest` |
| `19_module_review_and_interview_prep.py` | [19](../19-module-review-and-interview-prep.md) | The capstone mini pipeline |

## Quick start

```bash
cd examples
python 04_lists_and_intro_to_for_loops.py
python 17_robust_file_pipeline.py
pip install streamlit
python 18_test_orders_app.py
streamlit run 18_orders_app.py
```

## Notes

- Python 3.8 or newer. A few examples use newer features and say so.
- Files whose topic uses `input()` wait for you to type the answers. The documents show fixed sample answers.
- Some blocks inside the topic files raise an error on purpose, to show a rule. These are shown in the document without being run and are not in the example files.
- Examples create temporary files only inside the system temp folder.
