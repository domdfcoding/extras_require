#!/usr/bin/env python3
"""
The "extras_require" directive.

:copyright: Copyright (c) 2020 by Dominic Davis-Foster <dominic@davis-foster.co.uk>
:license: BSD, see LICENSE for details.
"""

# stdlib
import pathlib
import textwrap
import warnings
from typing import Any, Dict, Iterable, List, Union

# 3rd party
from docutils import nodes
from docutils.statemachine import ViewList
from domdf_python_tools.paths import PathPlus
from packaging.requirements import InvalidRequirement, Requirement
from sphinx.util.docutils import SphinxDirective

# this package
from sphinxcontrib.extras_require.sources import sources


class ExtrasRequireDirective(SphinxDirective):
	"""
	Directive to show a notice to users that a module, class or function has additional requirements.
	"""

	has_content: bool = True
	required_arguments: int = 1
	option_spec = {source[0]: source[2] for source in sources}  # type: ignore
	option_spec["scope"] = str

	def run(self) -> List[nodes.Node]:
		"""
		Create the extras_require node.

		:return:
		"""

		extra: str = self.arguments[0]

		targetid = f'extras_require-{self.env.new_serialno("extras_require"):d}'
		targetnode = nodes.target('', '', ids=[targetid])

		valid_requirements = get_requirements(
				env=self.env,
				extra=extra,
				options=self.options,
				content=self.content,
				)

		if not valid_requirements:
			warnings.warn("No requirements specified! No notice will be shown in the documentation.")
			return [targetnode]

		scope = self.options.get("scope", "module")

		content = make_node_content(valid_requirements, self.env.config.project, extra, scope=scope)
		view = ViewList(content.split("\n"))

		extras_require_node = nodes.attention(rawsource=content)
		self.state.nested_parse(view, self.content_offset, extras_require_node)  # type: ignore

		if not hasattr(self.env, "all_extras_requires"):
			self.env.all_extras_requires = []  # type: ignore

		self.env.all_extras_requires.append({  # type: ignore
			"docname": self.env.docname,
			"lineno": self.lineno,
			"extras_require": extras_require_node.deepcopy(),
			"target": targetnode,
			})

		return [targetnode, extras_require_node]


def validate_requirements(requirements_list: List[str]) -> List[str]:
	"""
	Validate a list of :pep:`508` requirements and format them consistently.

	:param requirements_list: List of :pep:`508` requirements.

	:return: List of :pep:`508` requirements with consistent formatting.
	"""

	valid_requirements = []

	for req in requirements_list:
		if req:
			try:
				valid_requirements.append(Requirement(req))
			except InvalidRequirement as e:
				raise ValueError(f"Invalid requirement '{req}': {str(e)}") from None

	valid_requirements.sort(key=lambda r: r.name)

	return [str(x) for x in valid_requirements]


def make_node_content(
		requirements: List[str],
		package_name: str,
		extra: str,
		scope: str = "module",
		) -> str:
	"""
	Create the content of an extras_require node.

	:param requirements: List of additional :pep:`508` requirements.
	:param package_name: The name of the module/package on PyPI.
	:type package_name: str
	:param extra: The name of the "extra".
	:type extra: str
	:param scope: The scope of the additional requirements, e.g. ``"module"``, ``"package"``.
	:type scope: str

	:return: The content of an extras_require node.
	:rtype:
	"""

	requirements_string = textwrap.indent("\n".join(requirements), "    ")

	if len(requirements) > 1:
		plural = 's'
	else:
		plural = ''

	content = f"""\
This {scope} has the following additional requirement{plural}:

.. code-block:: text

{requirements_string}

These can be installed as follows:

	.. code-block:: bash

		$ python -m pip install {package_name}[{extra}]

"""

	content = content.replace("\t", "    ")

	return content


def get_requirements(env, extra: str, options: Dict[str, Any], content: Union[Iterable, ViewList]) -> List[str]:
	"""
	Get the requirements for the extras_require node.

	:param env:
	:type env:
	:param extra:
	:type extra: str
	:param options:
	:param content:

	:return:
	"""

	n_sources = 0
	if list(content):
		n_sources += 1
	for source in sources:
		if (source[0] in options) and options[source[0]]:
			n_sources += 1

	if n_sources > 1:
		raise ValueError("Please specify only one source for the extra requirements")
	elif n_sources == 0:
		raise ValueError(f"Please specify a source for the extra requirements {extra}")

	src_dir = PathPlus(env.srcdir)
	package_root = src_dir.parent / env.config.package_root

	requirements: List[str]

	for option_name, getter_function, validator_function in sources:

		if option_name in options:
			requirements = getter_function(package_root, options, env, extra)
			break
	else:
		requirements = list(content)

	valid_requirements = validate_requirements(requirements)

	return valid_requirements
