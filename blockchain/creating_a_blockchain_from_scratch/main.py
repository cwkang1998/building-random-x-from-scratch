from blockchain import Blockchain

chain = Blockchain()

chain.add_new_block("First")
chain.add_new_block("Second")
chain.add_new_block("Third")
chain.add_new_block("Forth")
chain.add_new_block("Fifth")

for b in chain.blocks:
    print(b)
