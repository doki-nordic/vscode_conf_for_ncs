
import { Updater } from "use-immer";


export class ActionsBase<T> {
    protected draft = undefined as unknown as T;
    constructor(setState: Updater<T>) {
        console.log('This should not happen!', setState);
    }
};


export function ActionsImmerAutomation<T extends { new(...args: any[]): {} }>(actionsClass: T): T {
    let cls = function (this: any, setState: Function) {
        this._setState = setState;
    }
    let props: any = {};
    for (let name in Object.getOwnPropertyDescriptors(actionsClass.prototype)) {
        if (name !== 'constructor') {
            props[name] = {
                get: function (this: any) {
                    return (...args: any[]) => {
                        this._setState((draft: any) => {
                            this.draft = draft;
                            actionsClass.prototype[name].apply(this, args);
                        });
                    }
                }
            }
        }
    }
    Object.defineProperties(cls.prototype, props);
    /* TODO: Inheritance, this is old implementation:
    for (let name in Object.getOwnPropertyDescriptors(Object.getPrototypeOf(actionsClass.prototype))) {
      if (name !== 'constructor') {
        cls.prototype[name] = actionsClass.prototype[name];
      }
    }*/
    return cls as unknown as T;
}
