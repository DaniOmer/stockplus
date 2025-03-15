"""
Virus scanning utilities for the user module.
This module contains utilities for scanning files for viruses using ClamAV.
"""

import logging
import socket
from django.conf import settings

logger = logging.getLogger(__name__)

class VirusScanner:
    """
    Utility class for scanning files for viruses using ClamAV.
    """
    
    @staticmethod
    def scan_file(file):
        """
        Scan a file for viruses using ClamAV.
        
        Args:
            file: The file to scan
            
        Returns:
            tuple: (is_clean, message)
                is_clean: True if the file is clean, False if it contains a virus
                message: A message describing the result of the scan
        """
        if not settings.USE_CLAMAV:
            logger.warning("ClamAV scanning is disabled. Skipping virus scan.")
            return True, "Virus scanning is disabled"
        
        try:
            # Reset file pointer to beginning
            file.seek(0)
            
            # Connect to ClamAV daemon
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((settings.CLAMAV_HOST, settings.CLAMAV_PORT))
            
            # Send INSTREAM command
            sock.sendall(b'zINSTREAM\0')
            
            # Read file in chunks and send to ClamAV
            chunk_size = 4096
            while True:
                chunk = file.read(chunk_size)
                if not chunk:
                    break
                
                # Send chunk size as 4-byte unsigned integer in network byte order
                size = len(chunk).to_bytes(4, byteorder='big')
                sock.sendall(size)
                sock.sendall(chunk)
            
            # Send zero-length chunk to indicate end of file
            sock.sendall(b'\x00\x00\x00\x00')
            
            # Get response from ClamAV
            response = sock.recv(4096).decode('utf-8')
            sock.close()
            
            # Reset file pointer to beginning
            file.seek(0)
            
            # Parse response
            if 'INSTREAM size limit exceeded' in response:
                logger.warning(f"ClamAV size limit exceeded: {response}")
                return False, "File too large for virus scanning"
            elif 'FOUND' in response:
                virus_name = response.split('FOUND')[0].strip()
                logger.warning(f"Virus found: {virus_name}")
                return False, f"Virus detected: {virus_name}"
            else:
                logger.info("File is clean")
                return True, "File is clean"
        
        except Exception as e:
            logger.error(f"Error scanning file for viruses: {str(e)}")
            # Reset file pointer to beginning
            file.seek(0)
            return True, f"Error scanning file: {str(e)}"
