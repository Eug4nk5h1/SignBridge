# Adding or replacing sign videos

This project plays local clips from `assets/signs/`. The corresponding row in
`data/sign_catalog.json` determines which gloss uses each filename. Keep the
filename in the catalog and the filename on disk identical.

## Find and review a candidate

1. Open [ASL Signbank](https://aslsignbank.com/).
2. Search the project's **gloss** using **Search gloss**. If that gives no useful
   result, search the intended English meaning using **Search translation**.
3. Open candidate entries and play the video. A search result is only a
   candidate: compare the entry's gloss, translation equivalents, and signing
   variant with the intended meaning in your sentence.
4. Ask a fluent ASL signer to confirm the match before using it as an
   instructional example. Signbank describes itself as a documentation tool,
   not a teaching resource, and it documents variants rather than declaring
   one universally correct sign.
5. Copy the entry's full URL and note its attribution and license details. Do
   not use a draft video. The site's reuse information says to link directly to
   the Signbank entry when sharing its video.

## Replace one clip on your Mac

1. In Finder, open the SignBridge repository folder, then open `assets/signs/`.
2. Open `data/sign_catalog.json` in a text editor and find the entry by its
   `gloss`. Read its `video_file`, for example `friend.mp4`.
3. On the chosen Signbank entry, use the video's context menu and choose the
   option to save/download the video. Save the downloaded file somewhere easy
   to find, such as Downloads. If your browser does not offer a video download,
   use the Signbank page as the source link only and ask the instructor or
   Signbank team about an authorized copy; do not use a screen recording.
4. Rename the downloaded file to exactly the `video_file` value from the
   catalog, including lowercase spelling and `.mp4` extension. Move it into
   `assets/signs/` and choose **Replace** when Finder asks. Keep a backup of the
   old clip until you have checked the new one.
5. Update the same catalog entry with its source details, for example:

   ```json
   "video_file": "friend.mp4",
   "source_name": "ASL Signbank",
   "source_url": "https://aslsignbank.com/dictionary/gloss/ENTRY_ID.html",
   "license": "CC BY-NC-SA 4.0",
   "attribution": "ASL Signbank; actor/creator as credited on the entry"
   ```

   Replace `ENTRY_ID` and the attribution with the actual entry information.
   Keep valid JSON: commas belong between fields, but not after the final
   field in an object. Record any changes you made to the video; do not imply
   the original clip is unmodified if it was edited.
6. Reopen the SignBridge website, translate a sentence that produces this
   gloss, and confirm that the new clip plays and shows the intended sign.
7. In GitHub Desktop, review the changed video and catalog row, commit both
   together, then push the commit to your branch. The video files use Git LFS,
   so keep Git LFS enabled when committing and pushing.

## Attribution and project limitations

ASL Signbank lists its content under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).
Credit the source and link the exact entry wherever the project displays or
shares the clip. This license is for noncommercial use and requires
ShareAlike when distributing adaptations. Check the entry and current license
terms before reusing a video outside a class project.

This prototype maps a gloss to one isolated clip. That does not produce a
grammatical ASL sentence and can omit word order, facial expression, spatial
grammar, and context. Present it as a vocabulary-level demonstration, not as
a reliable translation for communicating a complete spoken message.
