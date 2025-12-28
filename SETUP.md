# Windows 11 Setup and Installation Guide

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Pre-Installation Checklist](#pre-installation-checklist)
3. [Installation Steps](#installation-steps)
4. [Post-Installation Configuration](#post-installation-configuration)
5. [Software Installation](#software-installation)
6. [System Optimization](#system-optimization)
7. [Security Configuration](#security-configuration)
8. [Troubleshooting](#troubleshooting)
9. [Additional Resources](#additional-resources)

---

## System Requirements

### Minimum Hardware Requirements for Windows 11

- **Processor**: 1 GHz or faster with 2 or more cores (compatible with x64 instruction set)
- **RAM**: 4 GB minimum (8 GB recommended)
- **Storage**: 64 GB SSD minimum (128 GB recommended for optimal performance)
- **Firmware**: UEFI capable
- **TPM**: Version 2.0 (required for Windows 11)
- **Graphics**: Compatible with DirectX 9 or later

### Recommended Hardware Specifications

- **Processor**: Intel Core i5/i7 (10th gen or newer) or AMD Ryzen 5/7 (3000 series or newer)
- **RAM**: 16 GB or more
- **Storage**: 256 GB+ NVMe SSD
- **Display**: 1920x1080 resolution or higher

---

## Pre-Installation Checklist

### Before You Begin

- [ ] **Backup Important Data**: Create complete backups of all important files
- [ ] **Check Compatibility**: Verify hardware compatibility with Windows 11
- [ ] **Create Installation Media**: Prepare USB drive (8 GB minimum)
- [ ] **Document Current Setup**: Note installed programs and configurations
- [ ] **Disable Antivirus**: Temporarily disable third-party antivirus during installation
- [ ] **Ensure Power Supply**: Connect device to power or ensure full battery charge
- [ ] **Check BIOS Settings**: Verify TPM 2.0 and Secure Boot are enabled
- [ ] **Internet Connection**: Ensure stable internet connection for driver downloads

### Required Tools and Materials

- USB Drive (8 GB or larger)
- Windows 11 Installation Media
- Product Key (if required)
- All hardware drivers (motherboard, GPU, etc.)
- Ethernet cable or WiFi information

---

## Installation Steps

### Step 1: Create Windows 11 Installation Media

#### Using Windows 11 Installation Assistant

1. Download Windows 11 Installation Assistant from Microsoft
2. Run the installer
3. Accept the license terms
4. Select "Create installation media for another PC"
5. Choose language, edition, and architecture (x64 for 64-bit)
6. Select USB Flash Drive option
7. Insert USB drive and follow prompts
8. Wait for media creation to complete

#### Using Media Creation Tool (Alternative)

1. Download Media Creation Tool from Microsoft
2. Run as Administrator
3. Select "Create installation media (USB flash drive, DVD, or ISO file)"
4. Select USB flash drive as media
5. Complete the process

### Step 2: BIOS Configuration

1. **Restart your computer** and enter BIOS (typically F2, F10, DEL, or ESC during startup)
2. **Enable TPM 2.0**:
   - Navigate to Security settings
   - Find TPM option
   - Ensure it's enabled
3. **Enable Secure Boot**:
   - Locate Secure Boot setting
   - Set to "Enabled"
4. **Set Boot Priority**:
   - Set USB as first boot device
   - Save and exit BIOS (F10 or designated save key)

### Step 3: Boot from Installation Media

1. Insert USB drive with Windows 11 installation media
2. Restart your computer
3. Press the appropriate key to boot from USB (usually F12, ESC, or DEL)
4. Select USB drive from boot menu
5. Windows Setup screen should appear

### Step 4: Windows 11 Installation

1. **Language and Regional Settings**:
   - Select your language
   - Select your region
   - Select your keyboard layout
   - Click "Next"

2. **Install Windows**:
   - Click "Install Now"
   - Enter Product Key if prompted (or select "I don't have a product key" for later)
   - Accept license terms

3. **Select Installation Type**:
   - Choose "Custom: Install Windows only" for clean installation
   - Or "Upgrade" if installing over existing Windows

4. **Disk Selection and Partitioning**:
   - Select target drive/partition
   - Delete existing partitions if performing clean install (back up data first!)
   - Let Windows create necessary partitions automatically
   - Click "Next" to begin installation

5. **Installation Process**:
   - Windows will copy files and install (may take 15-30 minutes)
   - Computer will restart multiple times
   - Do not interrupt or power off during this process

### Step 5: Initial Windows Setup

1. **Remove Installation Media**: Eject USB drive after installation completes

2. **Regional Settings**:
   - Confirm region and keyboard layout
   - Add additional layouts if needed

3. **Network Connection**:
   - Connect to WiFi or Ethernet
   - Skip if using Ethernet

4. **User Account Creation**:
   - Create local account or sign in with Microsoft account
   - Set username and password
   - Add security questions if using local account

5. **Device Privacy Settings**:
   - Review and configure privacy settings
   - Enable/disable telemetry, activity history, etc.

6. **Windows Update**:
   - Check for and install all available updates
   - May require additional restarts

---

## Post-Installation Configuration

### Initial System Configuration

#### 1. Install Drivers

```powershell
# Check for missing drivers in Device Manager
# Right-click on devices with warning symbols
# Update driver or download from manufacturer website
```

**Driver Installation Order**:
1. Chipset drivers
2. Network drivers (if not automatically installed)
3. Graphics drivers (GPU)
4. Sound drivers
5. Other peripheral drivers

#### 2. Configure Windows Updates

1. Open Settings (Win + I)
2. Navigate to "Update & Security"
3. Check for updates
4. Set update schedule to avoid work hours
5. Enable automatic updates

#### 3. Activate Windows

```powershell
# Command Prompt (as Administrator)
slmgr /ato
# Or manually activate through Settings > System > Activation
```

#### 4. Configure Storage

1. **Disable Hibernation** (if SSD space is limited):
```powershell
powercfg /h off
```

2. **Configure Disk Cleanup**:
   - Open Storage Settings
   - Run Disk Cleanup for C: drive
   - Enable Storage Sense

#### 5. Adjust Power Settings

1. Open Settings > System > Power & battery
2. Set power plan (Balanced or High Performance)
3. Configure sleep and display settings
4. Adjust USB selective suspend as needed

### 6. Configure Display and Resolution

1. Right-click Desktop
2. Select "Display settings"
3. Adjust resolution and scaling
4. Configure multiple displays if applicable
5. Adjust refresh rate in Advanced display settings

### 7. Customize Taskbar and Start Menu

1. Right-click taskbar
2. Select "Taskbar settings"
3. Customize appearance and behavior
4. Pin frequently used apps to Start menu

---

## Software Installation

### Essential Software

#### Development Tools (if applicable)

```powershell
# Install using Chocolatey (package manager)
# First, install Chocolatey if not already installed
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Install Node.js
choco install nodejs

# Install Python
choco install python

# Install Git
choco install git

# Install Visual Studio Code
choco install vscode
```

#### System Utilities

- **7-Zip**: File compression
- **VLC Media Player**: Video player
- **Firefox/Chrome**: Web browsers
- **Notepad++**: Text editor
- **.NET Framework**: Runtime environment

#### Office and Productivity

- Microsoft Office 365
- LibreOffice (free alternative)
- Adobe Reader
- Thunderbird (email client)

### Installation Best Practices

1. Install from official sources only
2. Disable unnecessary startup programs
3. Keep antivirus software updated
4. Use Windows Defender if no third-party antivirus
5. Regularly check for software updates

---

## System Optimization

### Performance Optimization

#### 1. Disable Unnecessary Startup Programs

```powershell
# Open Task Manager (Ctrl + Shift + Esc)
# Go to Startup tab
# Disable non-essential programs
```

#### 2. Adjust Visual Effects

```powershell
# For better performance on older hardware:
# Settings > System > About > Advanced system settings
# Performance > Visual Effects > Adjust for best performance
```

#### 3. Enable XMP/DOCP in BIOS

1. Restart and enter BIOS
2. Find XMP (Intel) or DOCP (AMD) setting
3. Enable for RAM performance boost
4. Save and exit

#### 4. SSD Optimization

```powershell
# Enable AHCI mode in BIOS (usually default)
# Disable defragmentation (not needed for SSD)
# Enable Trim:
fsutil behavior set DisableDeleteNotify 0
```

### 5. Disk Space Management

```powershell
# Remove temporary files
Remove-Item C:\Windows\Temp\* -Force -Recurse

# Disk Cleanup utility
cleanmgr

# Storage Sense settings
# Settings > System > Storage > Storage Sense
```

### 6. Memory Management

```powershell
# Monitor RAM usage via Task Manager
# Close unnecessary background applications
# Increase virtual memory if needed
```

---

## Security Configuration

### Essential Security Measures

#### 1. Windows Defender Firewall

```powershell
# Enable Firewall (usually enabled by default)
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True

# View firewall status
Get-NetFirewallProfile
```

#### 2. Windows Defender (Antivirus)

1. Open Settings > Privacy & Security
2. Virus & threat protection
3. Manage settings
4. Enable Real-time protection
5. Enable Cloud-delivered protection
6. Schedule regular scans

#### 3. Windows Update Security

```powershell
# Force Windows Update check
# Settings > Update & Security > Check for updates
```

#### 4. User Account Control (UAC)

1. Settings > Accounts > Other users
2. Configure UAC level (3 or 4 recommended)
3. Never disable completely

#### 5. Password Policy

1. Create strong passwords (12+ characters)
2. Use mix of uppercase, lowercase, numbers, symbols
3. Enable BitLocker for disk encryption:

```powershell
# Check BitLocker status
manage-bde -status

# Enable BitLocker on C: drive
manage-bde -on C:
```

#### 6. Network Security

```powershell
# Disable IPv6 if not needed
netsh int ipv6 set state disabled=yes

# Configure DNS (use 8.8.8.8 or 1.1.1.1)
# Settings > Network & Internet > Ethernet/WiFi > DNS settings
```

#### 7. Disable Unnecessary Services

```powershell
# Open Services (services.msc)
# Disable services not needed for your use case
# Examples: Print Spooler, Bluetooth Service (if not used)
```

---

## Troubleshooting

### Common Issues and Solutions

#### 1. Installation Hangs or Freezes

- **Solution**: 
  - Remove USB drive and restart
  - Update BIOS before installation
  - Try different USB port
  - Disable XMP in BIOS during installation

#### 2. Missing Drivers

- **Solution**:
  - Download from manufacturer website using another computer
  - Use Driver Booster or similar tool
  - Check Device Manager for unknown devices

#### 3. Windows Won't Activate

- **Solution**:
  - Verify product key is correct
  - Ensure internet connection
  - Run activation troubleshooter: Settings > Activation
  - Contact Microsoft support if issues persist

#### 4. Slow Performance

- **Solution**:
  - Check Task Manager for resource-heavy processes
  - Disable startup programs
  - Update drivers
  - Check for malware with Windows Defender
  - Increase available disk space

#### 5. Graphics Issues

- **Solution**:
  - Update GPU drivers to latest version
  - Adjust resolution and refresh rate
  - Disable hardware acceleration if needed
  - Update BIOS

#### 6. Network Issues

- **Solution**:
  - Update network drivers
  - Disable IPv6
  - Reset network settings:
```powershell
ipconfig /release
ipconfig /renew
```

#### 7. Boot Issues

- **Solution**:
  - Use Startup Repair (press F8 during boot)
  - Run System File Checker:
```powershell
sfc /scannow
```
  - Rebuild Boot Configuration Data:
```powershell
bootrec /RebuildBcd
```

---

## Additional Resources

### Official Documentation

- [Microsoft Windows 11 Documentation](https://learn.microsoft.com/en-us/windows/windows-11/)
- [Windows 11 System Requirements](https://support.microsoft.com/en-us/windows/windows-11-system-requirements-86c11283-ea52-4782-b8b7-2c19f16f1800)
- [Windows 11 User Guide](https://support.microsoft.com/en-us/windows/windows-11)

### Support and Help

- Microsoft Support: https://support.microsoft.com/
- Windows Community: https://answers.microsoft.com/
- Microsoft Docs: https://learn.microsoft.com/

### Useful Tools and Utilities

- **System Information**: `msinfo32`
- **Device Manager**: `devmgmt.msc`
- **Disk Management**: `diskmgmt.msc`
- **Event Viewer**: `eventvwr.msc`
- **Task Manager**: `taskmgr.exe`
- **Services**: `services.msc`
- **Registry Editor**: `regedit.exe` (use with caution)

---

## Quick Reference Commands

### PowerShell Commands (Run as Administrator)

```powershell
# Check Windows version
[System.Environment]::OSVersion

# Check system specifications
systeminfo

# Check disk space
Get-Volume

# Restart computer
Restart-Computer

# Shut down computer
Stop-Computer

# Create system restore point
Checkpoint-Computer -Description "My Restore Point"
```

### Keyboard Shortcuts

| Shortcut | Function |
|----------|----------|
| Win + I | Open Settings |
| Win + E | Open File Explorer |
| Win + X | Quick action menu |
| Win + V | Clipboard history |
| Win + Shift + S | Screenshot tool |
| Ctrl + Shift + Esc | Task Manager |
| Alt + Tab | Switch applications |

---

## Version History

- **v1.0** - December 28, 2025 - Initial comprehensive setup guide

---

**Last Updated**: December 28, 2025  
**Maintained By**: johny17111

For questions, issues, or suggestions, please refer to the project's issue tracker or contact the maintainer.
