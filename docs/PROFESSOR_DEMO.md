# Professor demo guide

## Two-minute walkthrough

1. **Introduce the aim (15 seconds).** “SignBridge is a prototype that demonstrates a speech-to-curated-sign-gloss pipeline. It is an educational prototype, not a fluent ASL translator.”
2. **Show the flow (20 seconds).** Walk through audio capture, Whisper transcription, spaCy token and dependency analysis, lexical normalization, exact catalog matching or WordNet candidate matching, controlled ASL gloss rules, concept/sign lookup, and local video checks. Expand **View the algorithm steps** to show the per-token decision trace.
3. **Run a known phrase (45 seconds).** Say clearly: “Where is your friend going?” Show the recognized sentence, the normalized sequence (`WHERE YOU FRIEND GO`), and the final output. Use **Start ASL** to play available clips.
4. **Show synonym and phrase matching (20 seconds).** Say: “My kinfolk come home.” The trace should show `kinfolk → FAMILY` with the `wordnet_context` method. Or say: “I don't know.” The phrase rule combines it into the single gloss `DONT_KNOW` and plays its phrase clip.
5. **Explain the mapping (20 seconds).** Expand **View the algorithm steps** and **View concept and resource mapping**. Point out that `FRIEND`, for example, resolves through a SignBridge-local concept ID and ASL sign ID to a video file. Explain that WordNet synonyms are only candidates and ambiguous expressions stay unresolved.
6. **Show a limitation (15 seconds).** Use a word outside the catalog or explain the unresolved notice. The app keeps the gloss visible and reports that it cannot play a clip for it.

## Expected result for the sample phrase

The rule-based translator is expected to produce the ordered glosses:

```text
WHERE YOU FRIEND GO
```

Each gloss should have a catalog mapping and available clip if the Git LFS assets were fetched. The exact Whisper transcript may vary with microphone and pronunciation. Demonstrate the matching stage with the expected sequence in the checks if audio recognition varies.

## Questions to be ready for

- **Is the output fluent ASL?** No. It is a controlled, rule-based gloss sequence with example videos.
- **Is synonym resolution contextual?** For expressions not found by an exact catalog match, the system can use WordNet sense relationships and context overlap to select a candidate. Ambiguous or unsupported items stay unresolved. This is a lightweight lexical method, not a trained semantic model.
- **Is WordNet available?** It is enabled after installing the Python dependency and downloading the corpus using the README setup step. Without it, exact catalog matches still work.
- **What are the IDs?** SignBridge-local concept and sign IDs used to connect glosses with catalog resources; they are not official identifiers.
- **What happens when a video is missing?** The gloss stays visible, the mapping status explains the missing resource, and the clip is omitted from playback.
- **What is the main contribution?** A working prototype that connects audio transcription, basic language analysis, deterministic normalization, explicit sign-resource mapping, and a visible failure path.
