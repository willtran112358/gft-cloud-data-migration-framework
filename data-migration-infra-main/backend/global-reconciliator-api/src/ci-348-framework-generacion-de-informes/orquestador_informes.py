"""Orquestador para ejecutar el rpoceso."""
from datetime import datetime

import findspark
from circular_071_reglas_especificas import DataProcessor as DataProcessorCircular071
from extract_df import ExtractDF
from reglas_generales import DataProcessor as DataProcessorReglas_Generales


findspark.init()


processor071 = DataProcessorCircular071("N")
processorGen = DataProcessorReglas_Generales("N")
extract = ExtractDF(processorGen.project_id)
exec_env = processorGen.exec_environment

class OrquestadorInformes:

    def __init__(self):
        if processorGen.project_id != processorGen.project_id_save and processorGen.project_id_save != "":
                self.project_id = processorGen.project_id
                self.project_id_save = processorGen.project_id_save
        else:
                self.project_id = processorGen.project_id
                self.project_id_save = processorGen.project_id

    def generate(self):
        """Funcion que ejecuta la ETL."""
        variables = processorGen.informa["Tablas"]["datos_a_extraer"].items()
        n_tables = len(variables)
        if n_tables > 1 :
            join = "Y"
        else:
            join = "N"
        hora_actual_1 = datetime.now()
        df_data = extract.extract_data(
            processorGen.informa, processorGen.informa, join
        ).repartition(100)
        df_data.cache()
        df_data = processor071.validar_ndi(df_data,"NDI","TDI")
        df_data = processor071.validar_fer(df_data)
        df_data = processor071.validar_loc(df_data)
        df_data = processorGen.aplicar_casteo_columnas_homologar(
            df_data, processorGen.homologacion
        )
        df_data = processorGen.homologar(processorGen.homologacion, df_data)
        df_data = processorGen.filtrar_por_columna_no_vacia(df_data)
        ############## Implementacion de Reglas ################
        df_data = processorGen.eliminar_duplicados_ultima_vigencia(
            df_data, ["NDI", "FAF"], "FECHA_PRESTACION"
        )
        df_data = processorGen.eliminar_nulos(df_data, "NDI")
        df_data = processorGen.validar_campo_sexo(df_data)
        df_data = processorGen.validar_fechas(df_data, ["FEN", "FAF"])
        df_data = processorGen.validar_traslado_efectivo(df_data)
        df_data = processor071.asignar_valor_car(df_data)
        df_data = processorGen.dividir_salario(df_data)
        df_data = processorGen.create_cod(df_data)
        df_data = processorGen.add_cda(df_data)
        df_data = processorGen.causa_retiro(df_data)
        df_data = processorGen.convertir_formato_fecha(df_data)
        df_data = processorGen.clear_columns(df_data)
        df_data = processor071.val_sal(df_data)
        df_validado_sal = processor071.validar_salario(df_data)
        df_seleccion_col = processorGen.seleccionar_columnas(df_validado_sal)
        path_file_select = processorGen.informe_general(
            df_seleccion_col, "/app/output_files/seleccion"
        )
        path_file_validado = processorGen.informe_general(
            df_validado_sal, "/app/output_files/validado"
        )
        val_file_nm = processorGen.upload_folder_to_gcp(self.project_id,exec_env["BUCKET_NAME"], path_file_validado)
        select_file_nm = processorGen.upload_folder_to_gcp(self.project_id,exec_env["BUCKET_NAME"], path_file_select)
        log_file_nm = processorGen.upload_folder_to_gcp(self.project_id, exec_env["BUCKET_NAME"], "logs")

        processorGen.load_csv_to_bigquery(select_file_nm,exec_env["BUCKET_NAME"], "Circular0071", self.project_id_save, self.project_id, exec_env["TB_CARGA_CIRCULAR"],"circular071")
        processorGen.ingest_log_to_bigquery(log_file_nm, exec_env["BUCKET_NAME"], "log_circular0071", self.project_id_save, self.project_id, exec_env["TB_CARGA_LOG"])

        hora_actual_2 = datetime.now()
        tiempo_demora = hora_actual_2 - hora_actual_1
        print("Tiempo de demora:", tiempo_demora)
        df_data.unpersist()
        return df_data