import os
import sys

# Ensure the parent directory is in the path so we can import scriptLattes
# This is only needed if scriptLattes is not installed as a package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scriptLattes.grupo import Grupo

def main():
    # Helper to get constant path relative to this script
    current_dir = os.path.dirname(__file__)
    config_file = os.path.join(current_dir, 'teste-01.config')
    
    print(f"--- Running scriptLattes Manual Example ---")
    print(f"Loading configuration from: {config_file}")
    
    # Initialize the Group with the configuration file
    grupo = Grupo(config_file)
    
    # You can inspect or modify parameters programmatically
    print(f"Project Name: {grupo.obterParametro('global-nome_do_grupo')}")
    
    # Example: Overriding the JSON output directory programmatically
    # Custom output directory for this example
    custom_output = os.path.join(current_dir, 'manual_output_json')
    grupo.atualizarParametro('global-diretorio_de_saida_json', custom_output)
    print(f"Output JSON directory set to: {custom_output}")

    # 1. Load Data
    print("\n[1/3] Loading Lattes data...")
    grupo.carregarDadosCVLattes()

    # 2. Compile Information
    print("\n[2/3] Compiling lists...")
    grupo.compilarListasDeItems()

    # 3. Generate Output (JSON)
    print("\n[3/3] Generating JSON files...")
    grupo.gerarArquivosJSONIndividuais()
    
    print("\n--- Execution complete! ---")
    print(f"Total members processed: {len(grupo.listaDeMembros)}")
    print(f"Check the output in: {custom_output}")

if __name__ == "__main__":
    # Note: Run this script from the project root directory to ensure relative paths in config work correctly
    # python3 exemplo/manual_example.py
    main()
