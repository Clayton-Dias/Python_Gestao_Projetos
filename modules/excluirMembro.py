from flask import redirect, url_for

from functions.db_membro import delete_member


def mod_excluir_membro(mysql, membro_id):

    delete_member(mysql, membro_id)

    return redirect(url_for('listar_membros'))
