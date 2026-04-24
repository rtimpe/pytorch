"""
Python polyfills for typing
"""

from __future__ import annotations

import typing
from typing import Any

from ..decorators import substitute_in_graph


__all__ = [
    "paramspec_has_default",
    "paramspec_typing_prepare_subst",
    "paramspec_typing_subst",
    "typevar_has_default",
    "typevar_typing_prepare_subst",
    "typevar_typing_subst",
    "typevartuple_has_default",
    "typevartuple_typing_prepare_subst",
]


# ref: Objects/typevarobject.c typevar_has_default_impl
@substitute_in_graph(typing.TypeVar.has_default, can_constant_fold_through=True)
def typevar_has_default(self: typing.TypeVar) -> bool:
    return self.__default__ is not typing.NoDefault


# ref: Objects/typevarobject.c typevar_typing_subst (dispatches to _typevar_subst)
@substitute_in_graph(typing.TypeVar.__typing_subst__)
def typevar_typing_subst(self: typing.TypeVar, arg: Any) -> Any:
    return typing._typevar_subst(self, arg)


# ref: Objects/typevarobject.c typevar_typing_prepare_subst_impl
@substitute_in_graph(typing.TypeVar.__typing_prepare_subst__)
def typevar_typing_prepare_subst(
    self: typing.TypeVar, alias: Any, args: tuple[Any, ...]
) -> tuple[Any, ...]:
    params = alias.__parameters__
    i = params.index(self)
    if i < len(args):
        return args
    if i == len(args) and self.__default__ is not typing.NoDefault:
        return args + (self.__default__,)
    raise TypeError(
        f"Too few arguments for {alias}; actual {len(args)}, expected at least {i + 1}"
    )


# ref: Objects/typevarobject.c paramspec_has_default_impl
@substitute_in_graph(typing.ParamSpec.has_default, can_constant_fold_through=True)
def paramspec_has_default(self: typing.ParamSpec) -> bool:
    return self.__default__ is not typing.NoDefault


# ref: Objects/typevarobject.c paramspec_typing_subst (dispatches to _paramspec_subst)
@substitute_in_graph(typing.ParamSpec.__typing_subst__)
def paramspec_typing_subst(self: typing.ParamSpec, arg: Any) -> Any:
    return typing._paramspec_subst(self, arg)


# ref: Objects/typevarobject.c paramspec_typing_prepare_subst_impl
@substitute_in_graph(typing.ParamSpec.__typing_prepare_subst__)
def paramspec_typing_prepare_subst(
    self: typing.ParamSpec, alias: Any, args: tuple[Any, ...]
) -> tuple[Any, ...]:
    return typing._paramspec_prepare_subst(self, alias, args)


# ref: Objects/typevarobject.c typevartuple_has_default_impl
@substitute_in_graph(typing.TypeVarTuple.has_default, can_constant_fold_through=True)
def typevartuple_has_default(self: typing.TypeVarTuple) -> bool:
    return self.__default__ is not typing.NoDefault


# ref: Objects/typevarobject.c typevartuple_typing_prepare_subst_impl
@substitute_in_graph(typing.TypeVarTuple.__typing_prepare_subst__)
def typevartuple_typing_prepare_subst(
    self: typing.TypeVarTuple, alias: Any, args: tuple[Any, ...]
) -> tuple[Any, ...]:
    return typing._typevartuple_prepare_subst(self, alias, args)
