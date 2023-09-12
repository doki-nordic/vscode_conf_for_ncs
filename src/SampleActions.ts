import { ActionsBase, ActionsImmerAutomation } from "./ActionsAutomation";
import { send, sendDelayed } from "./server";
import { State } from "./state";

const idBuildArgs = Symbol();
const idFlashArgs = Symbol();


@ActionsImmerAutomation
export class SampleActions extends ActionsBase<State> {

  selectBoard(value: string) {
    this.draft.board.value = value;
    send({ type: 'setadd', name: 'board', value });
  }

  selectSample(value: string) {
    this.draft.sample.value = value;
    send({ type: 'setadd', name: 'sample', value });
  }

  selectBuildArgs(value: string) {
    this.draft.buildArgs.value = value;
    sendDelayed({ type: 'set', name: 'buildArgs', value }, idBuildArgs);
  }

  selectFlashArgs(value: string) {
    this.draft.flashArgs.value = value;
    sendDelayed({ type: 'set', name: 'flashArgs', value }, idFlashArgs);
  }
};
