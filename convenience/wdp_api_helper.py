"""Provides a way for secure password storage and retrival in Windows OS."""

import binascii
import win32crypt


def write_wdp_api_xml(xml_file: str, username: str, password: str) -> None:
    """
    Encrypts the provided password with currently logged-in user's credentials.

    Username will still be stored in plain text. The function uses Windows Data Protection API.
    Creates an xml file with the file name "xml_file" to store the credentials.
    This xml file is created only once using the user
    name and the password, then used at runtime using the read function below.

    original code:
    https://dev.to/samklingdev/use-windows-data-protection-api-with-python-for-handling-credentials-5d4j


        Parameters
        ----------
        xml_file : str, required
        username : str, required
        password : str, required

        Returns
        -------
        None
    """

    # encrypt the password with DPAPI.
    crypted_password = win32crypt.CryptProtectData(
        password.encode("utf-16-le"), None, None, None, None, 0
    )

    # Do some magic to return the password in the exact same format as if you would use Powershell.
    password_secure_string = binascii.hexlify(crypted_password).decode()

    # Use the same xml format as for powershells Export-Clixml,
    # just replace values for username and password.
    xml = f"""<Objs Version="1.1.0.1" xmlns="http://schemas.microsoft.com/powershell/2004/04">
    <Obj RefId="0">
        <TN RefId="0">
        <T>System.Management.Automation.PSCredential</T>
        <T>System.Object</T>
        </TN>
        <ToString>System.Management.Automation.PSCredential</ToString>
        <Props>
        <S N="UserName">{username}</S>
        <SS N="Password">{password_secure_string}</SS>
        </Props>
    </Obj>
    </Objs>"""

    with open(xml_file, "w", encoding="utf8") as file:
        file.write(xml)
        file.close()
    print("XML file has been created.")


def read_wdp_api_xml(xml_file: str) -> tuple[str, str]:
    """
    Reads and decrypts the encrypted password from the xml file provided as an argument.

    Returns username and password in plain text.

    original code:
    https://dev.to/samklingdev/use-windows-data-protection-api-with-python-for-handling-credentials-5d4j


        Parameters
        ----------
        xml_file : str, required

        Returns
        -------
        (username,password)
    """

    try:
        with open(xml_file, "r", encoding="utf-8") as f:
            xml = f.read()

            # Extract username and password from the XML since thats all we care about.
            username = xml.split('<S N="UserName">')[1].split("</S>")[0]
            password_secure_string = xml.split('<SS N="Password">')[1].split("</SS>")[0]

    except Exception as ex:
        console.log("Could not read auth xml file.")
        raise ex
    else:
        # CryptUnprotectDate returns two values, description and the password,
        # we dont care about the description, so we use _ as variable name.
        decrypted_password_string = win32crypt.CryptUnprotectData(
            binascii.unhexlify(password_secure_string), None, None, None, 0
        )[1]
        return username, decrypted_password_string.decode("utf-16")
