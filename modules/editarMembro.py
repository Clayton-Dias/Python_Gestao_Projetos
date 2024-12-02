from flask import render_template, request, redirect, url_for

from functions.db_membro import edit_member, get_member_by_id


def mod_editar_membro(mysql, membro_id):

    if request.method == 'POST':
        
        edit_member(mysql, membro_id)

        return redirect(url_for('listar_membros'))

    membro = get_member_by_id(mysql, membro_id)
    
    return render_template('editar_membro.html', membro=membro)
