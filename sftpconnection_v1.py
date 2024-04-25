import pysftp
import paramiko

class My_Connection(pysftp.Connection):
    def __init__(self, *args, **kwargs):
        try:
            if kwargs.get('cnopts') is None:
                kwargs['cnopts'] = pysftp.CnOpts()
        except pysftp.HostKeysException as e:
            self._init_error = True
            raise paramiko.ssh_exception.SSHException(str(e))
        else:
            self._init_error = False

        self._sftp_live = False
        self._transport = None
        super().__init__(*args, **kwargs)

    def __del__(self):
        if not self._init_error:
            self.close()

def test_conn():
    try:
        with My_Connection('1.2.3.4', username='root', password='') as sftp:
            l = sftp.listdir()
            print(l)
    except paramiko.ssh_exception.SSHException as e:
        print('SSH error, you need to add the public key of your remote in your local known_hosts file first.', e)

def get_files():
    host = 'test.rebex.net'
    port = 22
    username = 'demo'
    password= 'password'
    try:
        conn = pysftp.Connection(host=host,port=port,username=username, password=password)
        print("connection established successfully")
        current_dir = conn.pwd
        print('our current working directory is: ',current_dir)
        #conn.get('readme.txt')
        #conn.get('/pub/example/ResumableTransfer.png')

        #moving to the given path, then download the file given in get method.
        with conn.cd('pub/example/'):
            conn.get('ResumableTransfer.png')

        #for downloading multiple file from given path
        with conn.cd('pub/example/'):
            files = conn.listdir()
            for file in files:
                if (file[-4:]=='.png'):
                    conn.get(file)
                    print(file,' downloaded successfully ')
    except:
        print('failed to establish connection to targeted server')

if __name__ == '__main__':
    test_conn()
