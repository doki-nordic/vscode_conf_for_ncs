
const DELAYED_VALUES_SEND_TIMEOUT = 1000;

export type Timeout = ReturnType<typeof setTimeout>;

export interface ServerSetValue {
    type: 'set' | 'add' | 'setadd';
    name: 'board' | 'sample' | 'buildArgs' | 'flashArgs';
    value: string;
};

export interface ServerRefresh {
    type: 'refresh';
    name: 'boardList' | 'sampleList' | 'buildArgsList' | 'flashArgsList';
};

export type ServerMessage = ServerSetValue | ServerRefresh;

let messageQueue: ServerMessage[] = [];
let sendTimeout: Timeout | null = null;

function sendAllNow() {
    sendTimeout = null;
    console.log('Sending messages: ', messageQueue);
    messageQueue = [];
}

export function send(message: ServerMessage) {
    messageQueue.push(message);
    if (sendTimeout === null) {
        sendTimeout = setTimeout(sendAllNow, 1);
    }
}

let delayedMessagesWithId = new Map<symbol, ServerMessage>();
let delayedMessagesAnonymous: ServerMessage[] = [];
let delayedMessagesTimeout: Timeout | null = null;

function sendAllDelayedNow() {
    delayedMessagesTimeout = null;
    for (const [, message] of delayedMessagesWithId) {
        send(message);
    }
    delayedMessagesAnonymous.forEach(send);
    delayedMessagesWithId.clear();
    delayedMessagesAnonymous = [];
}

export function sendDelayed(message: ServerMessage, id?: symbol) {
    if (delayedMessagesTimeout !== null) {
        clearTimeout(delayedMessagesTimeout);
    }
    if (id) {
        delayedMessagesWithId.set(id, message);
    } else {
        delayedMessagesAnonymous.push(message);
    }
    delayedMessagesTimeout = setTimeout(sendAllDelayedNow, DELAYED_VALUES_SEND_TIMEOUT);
}


