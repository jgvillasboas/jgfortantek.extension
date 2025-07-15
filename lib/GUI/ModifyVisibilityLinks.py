def alterar_visibilidade_links_na_ui(template_name, link_names, visibilidade_ativar=True):
    import time
    from pywinauto import Application

    # Aguarda a janela abrir após o PostCommand
    time.sleep(2)

    try:
        app = Application(backend='uia').connect(title_re=".*Visibility/Graphics.*")
        dlg = app.window(title_re=".*Visibility/Graphics.*")

        # Vai para aba "Revit Links"
        dlg.child_window(title="Revit Links", control_type="TabItem").select()
        time.sleep(2)

        grid = dlg.child_window(auto_id="ID_TREEGRID_GRID", control_type="DataGrid")

        for row in grid.children():
            try:
                row_name = row.children()[0].window_text()
                if any(link_name in row_name for link_name in link_names):
                    # A célula 'Visível' geralmente está na segunda ou terceira coluna (ajustável)
                    target_cell = row.children()[1]
                    target_cell.click_input()
                    time.sleep(0.5)
                    target_cell.type_keys("{SPACE}")
                    print(f"Toggled visibility for link row: {row_name}")
            except Exception as e:
                print("Erro ao processar linha da grade:", e)

        dlg.child_window(title="OK", control_type="Button").click()
    except Exception as e:
        print("Erro ao automatizar janela de visibilidade:", e)