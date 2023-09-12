import { Button, MenuItem } from "@blueprintjs/core";
import { ItemPredicate, Select } from "@blueprintjs/select";
import { ReactNode } from "react";
import { ValueWithList } from "./state";


const defaultFilter: ItemPredicate<string> = (query, value, _index, exactMatch) => {
    const normalizedText = value.toLowerCase().trim();
    const normalizedQuery = query.toLowerCase().trim();
    if (exactMatch) {
        return normalizedText === normalizedQuery;
    } else {
        return normalizedText.indexOf(normalizedQuery) >= 0;
    }
};

function renderEmpty(value: string): ReactNode {
    return value === '' ? (<i style={{ color: 'gray' }}>(Empty string)</i>) : value;
}

export function SelectWithList({ value, newItemLabel, onSelect, onValueRender, onOpen }: {
    value: ValueWithList;
    newItemLabel?: string;
    onSelect: (value: string) => void;
    onValueRender?: (value: string) => ReactNode;
    onOpen?: () => void;
}) {
    return (<Select<string>
        items={value.list}
        onItemSelect={onSelect}
        createNewItemFromQuery={newItemLabel ? (q => q) : undefined}
        itemPredicate={defaultFilter}
        popoverProps={{ onOpening: onOpen }}
        fill={true}
        createNewItemRenderer={newItemLabel ? ((query, active, handleClick) => (
            <MenuItem
                icon="add" text={`${newItemLabel} "${query}"`}
                roleStructure="listoption"
                active={active}
                onClick={handleClick} />)) : undefined}
        itemRenderer={
            (itemValue, { handleClick, handleFocus, modifiers, index }) => (modifiers.matchesPredicate ? (
                <MenuItem
                    active={modifiers.active}
                    disabled={modifiers.disabled}
                    key={index}
                    onClick={handleClick}
                    onFocus={handleFocus}
                    roleStructure="listoption"
                    text={onValueRender?.call(null, itemValue) || renderEmpty(itemValue)}
                />
            ) : null)}
    >
        <Button
            fill={true}
            alignText="left"
            text={onValueRender?.call(null, value.value) || value.value}
            rightIcon="caret-down"
            intent={value.serverValue !== undefined && value.serverValue !== value.value ? "success" : undefined}
        />
    </Select>)
}


export function SuggestWithList({ value, newItemLabel, onSelect, onAdd, onValueRender, onOpen }: {
    value: ValueWithList;
    newItemLabel?: string;
    onSelect: (value: string) => void;
    onAdd?: (value: string) => void;
    onValueRender?: (value: string) => ReactNode;
    onOpen?: () => void;
}) {
    return (<Select<string>
        items={value.list}
        onItemSelect={selectedValue => {
            if (onAdd && value.list.indexOf(selectedValue) < 0) {
                onAdd(selectedValue);
            }
            onSelect(selectedValue);
        }}
        createNewItemFromQuery={newItemLabel ? (q => q) : undefined}
        itemPredicate={defaultFilter}
        popoverProps={{ onOpening: onOpen, autoFocus: false }}
        inputProps={{ placeholder: 'Type...', leftIcon: 'edit' }}
        query={value.value}
        onQueryChange={onSelect}
        fill={true}
        createNewItemRenderer={newItemLabel ? ((query, active, handleClick) => (
            <MenuItem
                icon="add" text={`${newItemLabel} "${query}"`}
                roleStructure="listoption"
                active={active}
                onClick={handleClick} />)) : undefined}
        itemRenderer={
            (itemValue, { handleClick, handleFocus, modifiers, index }) => (modifiers.matchesPredicate ? (
                <MenuItem
                    active={modifiers.active}
                    disabled={modifiers.disabled}
                    key={index}
                    onClick={handleClick}
                    onFocus={handleFocus}
                    roleStructure="listoption"
                    text={onValueRender?.call(null, itemValue) || renderEmpty(itemValue)}
                />
            ) : null)}
    >
        <Button
            fill={true}
            alignText="left"
            text={onValueRender?.call(null, value.value) || renderEmpty(value.value)}
            rightIcon="caret-down"
            intent={value.serverValue !== undefined && value.serverValue !== value.value ? "success" : undefined}
        />
    </Select>)
}