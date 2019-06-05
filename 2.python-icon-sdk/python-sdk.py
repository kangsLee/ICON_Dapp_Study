import os

from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider
from iconsdk.builder.transaction_builder import (DeployTransactionBuilder, CallTransactionBuilder)
from iconsdk.libs.in_memory_zip import gen_deploy_data_content
from iconsdk.wallet.wallet import KeyWallet
from iconsdk.signed_transaction import SignedTransaction
from iconsdk.builder.call_builder import CallBuilder
from iconsdk.exception import JSONRPCException
from util.repeater import retry

icon_service = IconService(HTTPProvider("http://localhost:9001/api/v3"))
DIR_PATH = os.path.abspath(os.path.dirname(__file__))
SCORE_PROJECT= os.path.abspath(os.path.join(DIR_PATH, './welcome'))
wallet = KeyWallet.load("./keystore_test1", "test1_Account")

print("address: ", wallet.get_address()) # Returns an address
print("private key: ", wallet.get_private_key()) # Returns a private key
print("balance: ", icon_service.get_balance("hxe7af5fcfd8dfc67530a01a0e403882687528dfcb")) # Returns a private key


@retry(JSONRPCException, tries=10, delay=1, back_off=2)
def get_tx_result() -> str:
    tx_result = icon_service.get_transaction_result(tx_hash)
    print("waiting a second for accepting score...\n")
    return tx_result["scoreAddress"]

@retry(JSONRPCException, tries=10, delay=1, back_off=2)
def get_tx(tx_hash) -> str:
    tx_result = icon_service.get_transaction_result(tx_hash)
    print("waiting a second for accepting score...\n")
    return tx_result

def call_score_method_welcome(score_address):
    _call = CallBuilder()\
        .from_(wallet.get_address())\
        .to(score_address)\
        .method("welcome")\
        .build()
    _result = icon_service.call(_call)
    print(_result)

def transaction_scrooge(score_address):
  params = {"_to": wallet.get_address(), "_ratio": 10}
  call_transaction = CallTransactionBuilder()\
      .from_(wallet.get_address())\
      .value(100_000_000_000_000_000_000)\
      .to(score_address) \
      .step_limit(100_000_000_000)\
      .nid(3) \
      .nonce(4) \
      .method("scrooge")\
      .params(params)\
      .build()
  signed_transaction = SignedTransaction(call_transaction, wallet)
  tx_hash = icon_service.send_transaction(signed_transaction)
  print(tx_hash)
  print(get_tx(tx_hash))

# 1. DeployTransactionBuilder
transaction = DeployTransactionBuilder()\
    .from_(wallet.get_address())\
    .step_limit(100_000_000_000)\
    .to("cx0000000000000000000000000000000000000000")\
    .nid(3)\
    .nonce(100)\
    .content_type("application/zip")\
    .content(gen_deploy_data_content(SCORE_PROJECT)) \
    .params("")\
    .build()

signed_transaction = SignedTransaction(transaction, wallet)
tx_hash = icon_service.send_transaction(signed_transaction)
print(tx_hash)

score_address = get_tx_result()
# 2. CallBuilder
call_score_method_welcome(score_address)
# 3. CallTransactionBuilder
transaction_scrooge(score_address)