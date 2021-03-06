
.. rst:directive:: extras-require

	The requirements can be specified in several ways:

	.. rst:directive:option:: file: requirements_file
		:type: string

		Shows the requirements from the given file.
		The file must contain a list of :pep:`508` requirements, one per line.

		The path is relative to the ``package_root`` variable given in ``conf.py``,
		which in turn is relative to the parent directory of the sphinx documentation.

	.. rst:directive:option:: __pkginfo__
		:type: flag

		Flag to indicate the requirements should be obtained from ``__pkginfo__.py``.

		This looks in the parent directory of the sphinx documentation for a file named ``__pkginfo__.py``.
		The requirements are imported as the variable ``extras_require``, which must be a dictionary mapping extras to a list of requirements.
		e.g.

		.. code-block:: python

			extras_require = {
				'extra_b': [
						"flask >=1.1.2",
						"click < 7.1.2",
						"sphinx ==3.0.3",
						]
				}

		The requirements can be generated programmatically in the ``__pkginfo__.py`` file during the import process.


	.. rst:directive:option:: setup.cfg
		:type: flag

		Flag to indicate the requirements should be obtained from ``setup.cfg``.

		This looks in the parent directory of the sphinx documentation for a file named ``setup.cfg``.
		This file must be readable by Python's :mod:`configparser` module,
		and contain the section ``[options.extras_require]``.
		e.g.

		.. code-block:: ini

			[options.extras_require]
			extra_c = faker; pytest; tox

		See https://setuptools.readthedocs.io/en/latest/setuptools.html#configuring-setup-using-setup-cfg-files for more information on ``setup.cfg``.


	Only one of the above options can be used in each directive.

	|

	**Manual requirements:**

	If none of the above options are provided the :pep:`508` requirements can instead be provided as the content of the directive.
	Each requirement must be on its own line, and there must be a blank line between the directive and the list of requirements.
	e.g.

	.. rest-example::

		.. extras-require:: dates

			pytz >=2019.1


	|

	**Other options:**


	.. rst:directive:option:: scope
		:type: string

		Specifies a different scope for additional requirements, such as package, module, class or function.

		Any string value can be supplied here.

		**Example**

		.. rest-example::

			.. extras-require:: foo
				:scope: class

				bar
				baz
