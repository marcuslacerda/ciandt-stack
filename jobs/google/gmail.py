# -*- coding: utf-8 -*-
# encoding: utf-8
from __future__ import print_function
import httplib2

import base64
from email.mime.text import MIMEText
import os
from apiclient import errors

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


# If modifying these scopes, delete your previously saved credentials
# at ~/.resources/gmail-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/gmail.send'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'

class GMail(object):
    """docstring for GMail."""

    def __init__(self, flags):
        self.flags = flags

    def get_credentials(self):
        """Get valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.resources')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir, 'gmail-python-quickstart.json')

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            resource_path = os.path.join(credential_dir, CLIENT_SECRET_FILE)
            flow = client.flow_from_clientsecrets(resource_path, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if self.flags:
                credentials = tools.run_flow(flow, store, self.flags)
            else:
                # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials

    def create_message(self, sender, to, subject, message_text):
      """Create a message for an email.

      Args:
        sender: Email address of the sender.
        to: Email address of the receiver.
        subject: The subject of the email message.
        message_text: The text of the email message.

      Returns:
        An object containing a base64url encoded email object.
      """
      message = MIMEText(message_text)

      message['from'] = sender
      message['to'] = to
      message['cc'] = sender
      message['subject'] = subject
      return {'raw': base64.urlsafe_b64encode(message.as_string())}

    def send_message(self, service, user_id, message):
      """Send an email message.

      Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        message: Message to be sent.

      Returns:
        Sent Message.
      """
      try:
        message = (service.users().messages().send(userId=user_id, body=message)
                   .execute())
        print('Message Id: %s' % message['id'])
        return message
      except errors.HttpError, error:
        print('An error occurred: %s' % error)


    def get_service_gmail(self):
        """Shows basic usage of the Gmail API.

        Creates a Gmail API service object and outputs a list of label names
        of the user's Gmail account.
        """
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('gmail', 'v1', http=http)

        return service

    def send(self, to, subject, sheet_id, txt_error):

        from_mail = 'mlacerda@ciandt.com'
        #to_mail = 'mlacerda@ciandt.com'
        to_mail = '%s@ciandt.com' % to

        msg = 'Encontramos um erro ao processar o Mapa de Conhecimento Técnico do seu projeto \n\n'
        msg += 'https://docs.google.com/spreadsheets/d/%s \n\n' % str(sheet_id)
        msg += 'Problema encontrado:\n\n'
        msg += '  %s\n\n' % txt_error
        msg += 'Possíveis soluções: \n\n'
        msg += '  Erro [HttpError 403 when requesting]: Solução: Compartilhar acesso de leitura na planilha para mlacerda@ciandt.com ou para todos os usuarios do dominio ciandt \n\n'
        msg += '  Erro [could not convert string to float: #DIV/0!]: Solução: Revisar as fórmulas das colunas escondidas do lado direito da sheet Tecnology. Provavelmente você inclui novas linhas e não copiou as fórmulas dessas colunas. \n\n'
        msg += '  Erro [list index out of range]: Solução: Revisar as fórmulas das colunas escondidas do lado direito da sheet Tecnology. Provavelmente você inclui novas linhas e não copiou as fórmulas dessas colunas. \n\n\n\n'

        msg += 'Se o seu projeto não estiver utilizando essa planilha, pode removê-la. Obs: Lembre de exclui-la da lixeira do seu gdrive.\n\n'
        msg += 'Se o problema persistir entre em contato com Marcus Lacerda <mlacerda@ciandt.com> ou Leonel Togniolli <ltogniolli@ciandt.com>'

        service = self.get_service_gmail()

        message = self.create_message(from_mail, to_mail, subject, msg)
        self.send_message(service, from_mail, message)

if __name__ == '__main__':
    flags = []
    gmail = GMail(flags)
    subject = 'ACTION REQUIRED: Tech Gallery'
    gmail.send('mlacerda', subject, '1MAyEuRubYjzELnfbPnO8YPjS9jW-Xm26xTSXQdO_EWM', "texto erro")
