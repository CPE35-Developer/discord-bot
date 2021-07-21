import sympy
import discord_slash, discord
from sympy import Expr, solve, Symbol, Eq
from sympy.core.symbol import var

def string_to_expr(s: str) -> Expr:
    from sympy.parsing.sympy_parser import parse_expr
    from sympy.parsing.sympy_parser import parse_expr, \
        standard_transformations, implicit_multiplication_application, convert_xor

    transformations = (standard_transformations + (implicit_multiplication_application,) + (convert_xor,))
    expr = parse_expr(s, transformations=transformations)
    return expr

async def send_ans(ctx:discord_slash.SlashContext, ans:sympy.Expr, color:str="White"):
    sympy.preview(ans,viewer='file', filename='solve.png',dvioptions=['-D','200',"-bg", "Transparent","-fg",color])
    await ctx.send(file=discord.File('solve.png'))
    await ctx.channel.send(f'`{str(ans)}`')

async def solve_eq(ctx:discord_slash.SlashContext, equation:str, variable:str=None, color:str="White"):
    if '=' in equation:
        eqsplt = equation.split('=')
        expr = Eq(string_to_expr(eqsplt[0]), string_to_expr(eqsplt[1]))
    else:
        expr = string_to_expr(equation)
    
    if variable is None:
        ans = solve(expr)
    else:
        ans = solve(expr,Symbol(variable))
        
    await send_ans(ctx, ans, color)

