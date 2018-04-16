# DocumentX

## Overview

To create an easy way to consume *.docx files and allow the user the ability to specifically request sections programmatically for the consumption of data.
Using a structure similar to the core XML will be adapted and indexed off of the xml tags. The user will be left to extract the relevant groups and process
that data themselves.

## Design

A *.docx file is just a zipfile of XML and attachments (if included), stripping down these XML documents is crucial to the integrity of the data.

##### The XML Format

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:...>
    <w:body>
        <w:p w14:paraId="000000">
            <w:pPr>
                /* Styling options */
                <w:pStyle w:val="Title"/>
            </w:pPr>
            <w:r>
                <w:t>Text to for page</w:t>
            </w:r>
            <w:object>
                <v:shape>
                    <v:imagedata r:id="rId00" />
                </v:shape>
                /* Embedded document */
                <o:OLEObject r:id="rId00" ProgID="Excel.Sheet.12"/>
            </w:object>
        </w:p>
    </w:body>
</w:document>
```
