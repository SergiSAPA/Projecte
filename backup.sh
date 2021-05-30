#!/bin/bash

usuario=sergi
bdd=fixatges
carpetaCopias=backups/

mysqldump -u$usuario -pP@ssw0rd --databases $bdd > "$carpetaCopias"backup_$(date +%d-%m-%Y).sql
