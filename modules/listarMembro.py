from flask import render_template

from functions.db_membro import get_member


def mod_listar_membros(mysql):

    membros = get_member(mysql)
    
    return render_template('listar_membros.html', membros=membros)
