import fractions
import importlib
import json
import os
import os.path
import pathlib
import subprocess
import sys
import tempfile
import textwrap
import unittest

from tiledb.cloud._common import functions
from tiledb.cloud._vendor import cloudpickle


class SourceLinesTest(unittest.TestCase):
    def test_this_function(self):
        me = functions.getsourcelines(self.test_this_function)
        self.assertIsInstance(me, str)

    def test_missing_function(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            testfile = os.path.join(tmpdir, "bogus_module.py")
            with open(testfile, "w") as out:
                out.write(
                    textwrap.dedent(
                        """\
                        def unimportant_function(a):
                            pass
                        """
                    )
                )
            sys.path.insert(0, tmpdir)
            try:
                bogus = importlib.import_module("bogus_module")
            finally:
                sys.path.pop(0)
                sys.modules.pop("bogus_module", None)

            os.remove(testfile)
            self.assertIsNone(functions.getsourcelines(bogus.unimportant_function))

    def test_builtin(self):
        self.assertIsNone(functions.getsourcelines(dir))


class FuncableTest(unittest.TestCase):
    def test_good(self):
        class ImCallable:
            def __call__(self):
                pass

        items = (
            "registered/udf",
            len,
            lambda: None,
            self.test_good,
            functions.check_funcable,
            str.format,
            "".format,
            object,
            FuncableTest,
            ImCallable(),
        )
        for item in items:
            with self.subTest(item):
                functions.check_funcable(item=item)

    def test_bad(self):
        items = (
            5,
            object(),
            os.path,
        )
        for item in items:
            with self.subTest(item):
                with self.assertRaises(TypeError):
                    functions.check_funcable(item=item)


class ByValueTest(unittest.TestCase):
    def test_dedent(self):
        dedent_by_val = functions.to_register_by_value(textwrap.dedent)

        to_dedent = """
            here is some text
            it is indented
        """
        self.assertEqual(textwrap.dedent(to_dedent), dedent_by_val(to_dedent))

        twd_pickle = cloudpickle.dumps(textwrap.dedent)
        dbv_pickle = cloudpickle.dumps(dedent_by_val)

        self.assertNotEqual(twd_pickle, dbv_pickle)

    def test_across_processes(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = pathlib.Path(tmpdir)

            main_file = tmpdir_path / "dump_pickles"
            main_file.write_text(
                textwrap.dedent(
                    """\
                    #!/usr/bin/env python

                    import json

                    import cloudpickle
                    import the_module

                    from tiledb.cloud._common import functions

                    def uses_the_module():
                        # this has the_module in its globals.
                        return the_module.__name__

                    def imports_the_module():
                        # this does NOT have the_module in its globals.
                        import the_module
                        return the_module.__name__

                    def to_hex_pickles(**args):
                        return {
                            key: cloudpickle.dumps(value).hex()
                            for (key, value) in args.items()
                        }

                    def main():
                        ten_thirds_val = functions.to_register_by_value(
                            the_module.ten_thirds)
                        print(json.dumps(to_hex_pickles(
                            ten_thirds=the_module.ten_thirds,
                            ten_thirds_val=ten_thirds_val,
                            uses_the_module=uses_the_module,
                            imports_the_module=imports_the_module,
                            to_hex_pickles=to_hex_pickles,
                        )))

                    if __name__ == "__main__":
                        main()
                    """
                )
            )
            main_file.chmod(0o550)
            # When executing a Python file, the directory where the file
            # is located is placed at the start of sys.path, so the_module.py
            # will be accessible as the_module.
            mod_file = tmpdir_path / "the_module.py"
            mod_file.write_text(
                textwrap.dedent(
                    """
                    import fractions
                    def ten_thirds() -> fractions.Fraction:
                        return fractions.Fraction(10, 3)
                    """
                )
            )

            result = subprocess.run((main_file,), stdout=subprocess.PIPE, check=True)
            pickles = json.loads(result.stdout)

            def unpickle(key):
                return cloudpickle.loads(bytes.fromhex(pickles[key]))

            with self.assertRaises(ModuleNotFoundError):
                # Can't unpickle the function-by-reference.
                unpickle("ten_thirds")

            # Can unpickle the function-by-value.
            ten_thirds = unpickle("ten_thirds_val")
            self.assertEqual(fractions.Fraction(10, 3), ten_thirds())

            # Can't unpickle something that references the_module in globals.
            with self.assertRaises(ModuleNotFoundError):
                unpickle("uses_the_module")

            # Can unpickle something that imports the_module internally...
            imports_the_module = unpickle("imports_the_module")
            # ...but can't execute it.
            with self.assertRaises(ModuleNotFoundError):
                imports_the_module()

            # Functions defined in the __main__ module are always by-value.
            to_hex_pickles = unpickle("to_hex_pickles")
            self.assertEqual(
                {
                    "n": cloudpickle.dumps(None).hex(),
                    "z": cloudpickle.dumps(0).hex(),
                },
                to_hex_pickles(n=None, z=0),
            )

    def test_bad(self):
        for case in (
            int,  # built-in function
            int.bit_length,  # built-in unbound method
            "string".join,  # built-in bound method
            textwrap.TextWrapper,  # type
            textwrap.TextWrapper().fill,  # bound method
            os.path,
            88888,
        ):
            with self.assertRaises(TypeError, msg=f"not raised for {case}"):
                functions.to_register_by_value(case)
