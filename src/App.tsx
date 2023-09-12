import './App.css';
import "normalize.css/normalize.css";
import { initialState } from './state';
import { Button, ButtonGroup, Callout, Card, ContextMenu, ControlGroup, InputGroup, Section, SectionCard, Menu, MenuItem, Popover, MenuDivider, Slider, Switch, FormGroup, Checkbox } from '@blueprintjs/core';
import { SelectWithList, SuggestWithList } from './SelectWithList';
import { send } from './server';
import { useImmer } from 'use-immer';
import { SampleActions } from './SampleActions';


function sampleToElement(value: string) {
  let separator = Math.max(value.lastIndexOf('/'), value.lastIndexOf('\\'));
  return (<><span style={{ fontSize: '90%' }}>{value.substring(0, separator + 1)}</span><b>{value.substring(separator + 1)}</b></>);
}

function App() {
  const [state, setState] = useImmer(initialState);
  const actions = new SampleActions(setState);

  return (
    <div className="App">

      <Section icon="layer" title="Error" subtitle="Invalid Zephyr environment" rightElement={<Button intent="primary" text="Use Zephyr from workspace" />}><SectionCard>
        <Callout intent="danger">
          <table>
            <tr>
              <td>Workspace:</td>
              <td>/home/doki/work/ncs</td>
            </tr>
            <tr>
              <td>Sourced Zephyr:</td>
              <td>/home/doki/work/next</td>
            </tr>
          </table>
        </Callout>

      </SectionCard>
      </Section>

      &nbsp;<br />&nbsp;

      <Section icon="layer" title="Active Sample" subtitle="Workspace: /home/doki/work/ncs"><SectionCard>
        <table>
          <tbody>
            <tr>
              <td>Sample:</td>
              <td>
                <SelectWithList
                  value={state.sample}
                  newItemLabel='Create'
                  onSelect={actions.selectSample}
                  onOpen={() => send({ type: 'refresh', name: 'sampleList' })}
                  onValueRender={sampleToElement}
                />
              </td>
            </tr>
            <tr>
              <td>Board:</td>
              <td>
                <SelectWithList
                  value={state.board}
                  newItemLabel='Create'
                  onSelect={actions.selectBoard}
                  onOpen={() => send({ type: 'refresh', name: 'boardList' })}
                />
              </td>
            </tr>
            <tr>
              <td>Build arguments:</td>
              <td>
                <SuggestWithList
                  value={state.buildArgs}
                  newItemLabel='Add'
                  onSelect={actions.selectBuildArgs}
                  onAdd={value => send({ type: 'add', name: 'buildArgs', value })}
                  onOpen={() => send({ type: 'refresh', name: 'buildArgsList' })}
                />
              </td>
            </tr>
            <tr>
              <td>Flash arguments:</td>
              <td>
                <SuggestWithList
                  value={state.flashArgs}
                  newItemLabel='Add'
                  onSelect={actions.selectFlashArgs}
                  onAdd={value => send({ type: 'add', name: 'flashArgs', value })}
                  onOpen={() => send({ type: 'refresh', name: 'flashArgsList' })}
                />
              </td>
            </tr>
            <tr>
              <td>Flash SNR:</td>
              <td>
                <SuggestWithList
                  value={state.flashArgs}
                  newItemLabel='Add'
                  onSelect={actions.selectFlashArgs}
                  onAdd={value => send({ type: 'add', name: 'flashArgs', value })}
                  onOpen={() => send({ type: 'refresh', name: 'flashArgsList' })}
                />
              </td>
            </tr>
          </tbody>
        </table>
      </SectionCard><SectionCard>
          <ControlGroup>
            <Button text="Flash" intent='success' icon="play" />
            <Button text="Build" intent='primary' icon="build" />
            <Button text="Rebuild" intent="warning" icon="refresh" />
            <Button text="Purge" intent="danger" icon="delete" />
            <Button text="Menuconfig" icon="cog" />
            <Popover position='right-top'
              content={
                <Menu>
                  <MenuItem text="CMake" icon="code" />
                  <MenuItem text="GUI Config" icon="cog" />
                  <MenuItem text="Remote - GUI Config" icon="cog" />
                  <MenuItem text="Remote - Menuconfig" icon="cog" />
                  <MenuItem text="Delete" intent="danger" icon="trash">
                    <MenuItem text="Build folder" intent="danger" icon="dot" />
                    <MenuItem text="Build folders of this sample" intent="danger" icon="layer" />
                    <MenuItem text="Build folders of this workspace" intent="danger" icon="layers" />
                  </MenuItem>
                </Menu>
              }
            ><Button icon="double-chevron-right" />
            </Popover>
          </ControlGroup>
        </SectionCard></Section>

      &nbsp;<br />&nbsp;

      <Section icon="manual" title="Documentation" subtitle="Build directory: /home/doki/work/ncs/nrf/doc/_build"><SectionCard>
        <ControlGroup>
          <Button text="Open" intent='success' icon="play" />
          <ButtonGroup>
            <Button text="Build: nrf" intent='primary' icon="build" />
            <Popover position='bottom'
              content={
                <Menu>
                  <MenuItem text="all" icon="manual" />
                  <MenuDivider />
                  <MenuItem text="nrf" icon="book" />
                  <MenuItem text="nrfxlib" icon="book" />
                  <MenuItem text="zephyt" icon="book" />
                  <MenuItem text="mcuboot" icon="book" />
                  <MenuDivider />
                  <MenuItem text="First time build" icon="high-priority">
                    <MenuItem text="all" icon="manual" />
                  <MenuDivider />
                    <MenuItem text="nrf" icon="book" />
                    <MenuItem text="nrfxlib" icon="book" />
                    <MenuItem text="zephyt" icon="book" />
                    <MenuItem text="mcuboot" icon="book" />
                  </MenuItem>
                </Menu>
              }>
              <Button intent='primary' icon="caret-down" />
            </Popover>
          </ButtonGroup>
          <Button text="Build on save: yes" icon="tick" />
          <Popover position='right-top'
            content={
              <Menu>
                <MenuItem text="Delete" intent="danger" icon="trash" />
              </Menu>
            }>
            <Button icon="double-chevron-right" />
          </Popover>
        </ControlGroup>
      </SectionCard></Section>

      &nbsp;<br />&nbsp;

      <Section icon="layers" title="Boards" subtitle="Workspace: /home/doki/work/ncs"><SectionCard>
        <ControlGroup>
          <InputGroup value='329947732' style={{ width: 400 }} readOnly={true} rightElement={(
            <ButtonGroup>
              <Button text="ttyACM0" />
              <Button text="ttyACM1" />
              <Button text="Flash target" intent="success" />
            </ButtonGroup>
          )} />

        </ControlGroup>
      </SectionCard></Section>
    </div>
  );
}

export default App;
