$caracteristicasPersonalizadas = @{
    "Internet-Explorer-Optional-amd64"       = "Internet Explorer 11"
    "WindowsMediaPlayer"                     = "Windows Media Player"
    "Xps-Viewer"                              = "XPS Viewer"
    "Xps-Services"                            = "XPS Services"
    "WorkFolders-Client"                      = "Work Folders Client"
    "Printing-XPSServices-Features"           = "Microsoft Print to PDF"
    "FaxServicesClientPackage"                = "Fax and Scan"
    "MSRDC-Infrastructure"                    = "Remote Differential Compression"
    "MicrosoftWindowsPowerShellV2Root"        = "Windows PowerShell 2.0"
    "LegacyComponents"                        = "Legacy Components > DirectPlay"
}

Write-Host "`nObteniendo características instaladas en el sistema...`n" -ForegroundColor Cyan

# Obtener todas las características con su estado
$caracteristicasSistema = Get-WindowsOptionalFeature -Online

# Crear un diccionario para acceso rápido
$dicEstadoSistema = @{}
foreach ($car in $caracteristicasSistema) {
    $dicEstadoSistema[$car.FeatureName.ToLower()] = $car.State
}

Write-Host "Estado de características personalizadas:`n" -ForegroundColor Cyan

foreach ($clave in $caracteristicasPersonalizadas.Keys) {
    $nombreLegible = $caracteristicasPersonalizadas[$clave]
    $claveLower = $clave.ToLower()

    if ($dicEstadoSistema.ContainsKey($claveLower)) {
        $estadoRaw = $dicEstadoSistema[$claveLower]
        switch ($estadoRaw) {
            "Enabled" { $estadoLegible = "HABILITADO"; $color = "Green" }
            "Disabled" { $estadoLegible = "DESHABILITADO"; $color = "Yellow" }
            default { $estadoLegible = "DESCONOCIDO ($estadoRaw)"; $color = "Gray" }
        }
        Write-Host ("- {0} [{1}] : {2}" -f $nombreLegible, $clave, $estadoLegible) -ForegroundColor $color
    }
    else {
        Write-Host ("- {0} [{1}] : NO ENCONTRADO EN EL SISTEMA" -f $nombreLegible, $clave) -ForegroundColor Red
    }
}
