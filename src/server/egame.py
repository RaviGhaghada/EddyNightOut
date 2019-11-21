#! /usr/bin/python3
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import operator
import time
import threading
import sys
import os
from gui import GUI

# twilio phone-numbers:update "+441732252343" --sms-url="http://localhost:5000/sms"
# use code above to reset tunnel
num_reply = dict()
g = GUI()

app = Flask(__name__)


@app.route("/sms", methods=['GET', 'POST'])
def sms_ahoy_reply():
    resp = MessagingResponse()
    num_reply[request.form['From']] = request.form['Body']
    resp.message("Response Received")
    # print(num_reply)
    return str(resp)


def run_vote(story, index):

    g.addImage(index)

    currnode = story[index]
    
    # each line in currnode's text description, a list of strings
    for line in currnode.text:
        g.addtext(line)

    if (currnode.next_nodes) is None:
        return None
    if len(currnode.next_nodes) == 1:
        return currnode.next_nodes
    
    

    options = dict()
    g.addtext("Options are: ")
    # all the options for my current node
    for optionIndex in currnode.next_nodes:
        g.addtext("{} {}".format(optionIndex, story[optionIndex].label))
        options[optionIndex] = 0

    g.refresh()

    time.sleep(15)
    #num_reply['+447415961525'] = input("Vote: ")
    
    for vote in num_reply.values():
        if vote in options:
            options[vote] = options[vote]+1

    num_reply.clear()

    total = sum(options.values())
    if total == 0:
        g.addtext("Nobody voted.")
        return index

    # at this point, total cannot be zero
    g.addtext("{} people voted.".format(total))

    for key in options:
        g.addtext("{}% voted OPTION {}".format("%0.2f" % (options[key] / total * 100), key))

    return max(options, key=lambda key: options[key])


def create_tree(filepath):
    tree = {}
    story = []

    class Node:
        node = None
        next_nodes = None
        jump = False
        text = ""
        label = ""

        def __init__(self, label, textField, node, jump, next_nodes=None):
            self.next_nodes = next_nodes
            self.jump = jump
            self.node = node
            self.text = textField
            self.label = label

    def collect_text(file_as_list, index):
        y = index
        collected_lines = []
        while y < len(file_as_list) and not file_as_list[y].startswith('Op'):
            collected_lines.append(file_as_list[y])
            y += 1
        return collected_lines

    if not os.path.isfile(filepath):
        print("File path {} does not exist. Exiting...".format(filepath))
        sys.exit()

    with open(filepath, 'r', encoding="utf8") as fp:
        cnt = 0
        for line in fp:
            story.append(line)
            cnt += 1

    for i, line in enumerate(story):
        if line is None:
            None
        elif line.startswith('Op'):
            # Split into opcode + message
            split = story[i].split(':')
            # Collect text for the node
            text = collect_text(story, i + 1)
            # Collect connected nodes
            children = split[0].split(' ')

            # Display Node
            # Format: Op Node [Children]
            if len(split[0]) > 6:
                tree[children[1]] = (Node(split[1], text, children[1], False, children[2:]))

            # Jump Node
            # Format: Op Node Jump
            elif len(split[0]) == 6:
                tree[children[1]] = Node(split[1], text, children[1], True, children[2])

            # End node
            # Format: Op Node None
            else:
                tree[children[1]] = Node(split[1], text, children[1], False)

    return tree


class Game(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        story = create_tree("Storyline")
        curr = '0'

        while story[curr].node is not None:
            g.clear()
            curr = run_vote(story, curr)
            g.refresh()
            time.sleep(6)

if __name__ == "__main__":
    gem = Game()
    gem.start()
    app.run()
