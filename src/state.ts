
export interface ValueWithList {
    value: string;
    list: string[];
    serverValue?: string;
}

export interface State {
    board: ValueWithList;
    sample: ValueWithList
    buildArgs: ValueWithList;
    flashArgs: ValueWithList;
};

export const initialState: State = {
    board: { value: 'PCA10054', serverValue: 'PCA10054', list: ['PCA10054', 'PCA10100', 'PCA10095', 'Other'] },
    sample: { value: 'nrf/samples/bluetooth/cgm', serverValue: 'nrf/samples/bluetooth/cgm', list: ['nrf/samples/bluetooth/cgm', 'nrf/samples/blink'] },
    buildArgs: { value: '', serverValue: '', list: ['', '-DOVERLAY_FILE=second.conf', '-DLAYER=unknown-whatever'] },
    flashArgs: { value: '', serverValue: '', list: ['', '-O--ip -O192.133.', '-DWIFI_PASS=whatever'] },
};

/*


-rw-rw-r-- 1 doki doki  231 Sep  7 11:12 boards.mru.txt
-rw-rw-r-- 1 doki doki   19 Sep  7 11:12 board.txt
-rw-rw-r-- 1 doki doki  263 Sep  7 15:30 build_args.mru.txt
-rw-rw-r-- 1 doki doki    0 Sep  7 15:30 build_args.txt
-rw-rw-r-- 1 doki doki   14 Sep  7 10:17 checkpatchBase
-rw-rw-r-- 1 doki doki  212 Sep  7 10:17 exampleBoard
-rw-rw-r-- 1 doki doki  199 Feb 15  2022 exampleCmd
-rw-rw-r-- 1 doki doki 2047 Sep  7 10:17 exampleFolder
-rw-rw-r-- 1 doki doki   25 Sep  7 15:38 flash_args.mru.txt
-rw-rw-r-- 1 doki doki   25 Sep  7 15:38 flash_args.txt
-rw-rw-r-- 1 doki doki    0 Sep  6 08:47 instanceTitle.mru.txt
-rw-rw-r-- 1 doki doki   15 Sep  6 08:46 instanceTitles
-rw-rw-r-- 1 doki doki   14 Sep  6 09:30 instanceTitles.mru.txt
-rw-rw-r-- 1 doki doki   71 Sep  7 10:14 samples.mru.txt
-rw-rw-r-- 1 doki doki   38 Sep  7 11:00 sample.txt

*/