# A fictional author self-review

Everything here is invented for illustration. The paths, revision label, commands, and test outcomes are example data, not evidence of checks run on a real project. There are no real PR permalinks.

## Task and final diff

The request: retry transient failures for product lookups, with at most two attempts. Preserve the existing behavior for other request methods. The fictional final revision is `example-revision-1`.

```diff
diff --git a/src/catalog.ts b/src/catalog.ts
--- a/src/catalog.ts
+++ b/src/catalog.ts
@@ -1,3 +1,12 @@
 export async function request(url: string, init: RequestInit = {}) {
-  return fetch(url, init);
+  const method = (init.method ?? "GET").toUpperCase();
+  const attempts = method === "GET" ? 2 : 1;
+  for (let attempt = 1; attempt <= attempts; attempt++) {
+    try {
+      const response = await fetch(url, init);
+      if (response.status !== 503 || attempt === attempts) return response;
+    } catch (error) {
+      if (attempt === attempts) throw error;
+    }
+  }
 }
```

The new file's line 3 chooses the attempt count; lines 5–9 decide which failures get another attempt. Line numbers refer to this final diff and must be refreshed if it changes.

## Before

> Added retries. Tests pass. Please review carefully.

This gives the reviewer neither a useful decision to inspect nor the scope of the test evidence.

## After: draft inline comments

**`src/catalog.ts:3`, RIGHT side, `example-revision-1`:** This limits retries to GET, preserving the requested behavior for other methods. HEAD requests still receive only one attempt. Do catalog consumers rely on HEAD for availability checks, and should support for that method be a separate change?

**`src/catalog.ts:7`, RIGHT side, `example-revision-1`:** Only HTTP 503 responses are retried; the catch block also retries thrown fetch errors for GET. There is no delay between attempts. The focused tests below cover attempt counts, but there is no load-test evidence for behavior during an outage. Please confirm whether immediate retry is acceptable for this service's traffic budget.

## After: draft review summary

> Verification at `example-revision-1`: Passed — `npm test -- catalog.test.ts`, covering GET recovery after one 503, two-attempt exhaustion, a thrown fetch error, and POST remaining a single attempt. Those are existing tests; no new tests were added. Not run — full suite and load test, because this fictional environment contains only the focused test harness. Cross-module compatibility and outage traffic amplification remain unverified.
>
> Open decision: the service owner needs to confirm the outage traffic budget before this is considered ready. This author review is not independent approval.

## Delivery

With draft-only authority, return the notes above without posting. With publication authority on a specified PR, recheck its current head and existing comments, verify these anchors against that real diff, and submit a comment-only review. Read back the submitted review and return verified permalinks. If the head moved, refresh the notes first; if a previous submission may have succeeded, check before retrying.

The summary does not repeat the inline trade-off explanations. A later revision should add or update only material new information. Never manufacture a URL or submit an approval event for this self-review.
