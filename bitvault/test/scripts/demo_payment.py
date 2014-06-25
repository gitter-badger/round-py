import os.path
import yaml

import bitvault.test.scripts.helpers as helpers

from coinop.crypto.passphrasebox import PassphraseBox
from coinop.bit.multiwallet import MultiWallet

import bitvault


wallet_file = helpers.wallet_file()

if not os.path.isfile(wallet_file):
    message = u'''
    This script requires output from demo_account.rb, which will be
    found in {0}.
    Run demo_account.rb first, then fund the address provided using
    a testnet faucet.  Once the transaction has 3 confirmations,
    you should be able to run this script.
    '''.format(wallet_file)
else:
    with open(wallet_file, u'r') as file:
        data = yaml.load(file)

api_token = data[u'api_token']
passphrase = data[u'passphrase']
wallet_url = data[u'wallet'][u'url']
account_url = data[u'account'][u'url']

client = bitvault.authed_client(api_token=api_token)

wallet = client.applications.get().wallet(wallet_url).get()
account = wallet.account(account_url).get()

faucet_address = u'mx3Az5tkWhEQHsihFr3Nmj6mRHLeqtqfNK'

primary_seed = PassphraseBox.decrypt(passphrase, wallet.primary_private_seed)

multi_wallet = MultiWallet(
    private={u'primary': primary_seed},
    public={
        u'cosigner': wallet.cosigner_public_seed,
        u'backup': wallet.backup_public_seed})

unsigned_payment = account.payments.create(
    outputs=[{'amount': 6000000, 'payee': {'address': faucet_address}}])

#transaction = Transaction.from_data(unsigned_payment)
#change_output = transaction.outputs[-1]

#multi_wallet.is_valid_output(change_output)

#signatures = multi_wallet.signatures(transaction)
