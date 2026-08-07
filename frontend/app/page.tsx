"use client";

import { FormEvent, useEffect, useState } from "react";
import Image from "next/image";
import { ApiError, Video, createVideo, getVideos } from "@/lib/api";
import styles from "./page.module.css";

export default function Home() {
  const [videos, setVideos] = useState<Video[]>([]);
  const [url, setUrl] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [submitError, setSubmitError] = useState<string | null>(null);

  useEffect(() => {
    getVideos()
      .then(setVideos)
      .catch((err: unknown) => setLoadError(err instanceof ApiError ? err.message : "영상 목록을 불러오지 못했습니다."))
      .finally(() => setIsLoading(false));
  }, []);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitError(null);
    setIsSubmitting(true);
    try {
      const video = await createVideo(url);
      setVideos((prev) => [video, ...prev]);
      setUrl("");
    } catch (err) {
      setSubmitError(err instanceof ApiError ? err.message : "영상을 저장하지 못했습니다.");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <div className={styles.page}>
      <main className={styles.main}>
        <h1>유튜브 영상 보관함</h1>

        <form className={styles.form} onSubmit={handleSubmit}>
          <input
            className={styles.input}
            type="url"
            placeholder="https://www.youtube.com/watch?v=..."
            value={url}
            onChange={(event) => setUrl(event.target.value)}
            required
          />
          <button className={styles.button} type="submit" disabled={isSubmitting}>
            {isSubmitting ? "저장 중..." : "저장"}
          </button>
        </form>

        {submitError && <p className={styles.error}>{submitError}</p>}

        {isLoading ? (
          <p>불러오는 중...</p>
        ) : loadError ? (
          <p className={styles.error}>{loadError}</p>
        ) : videos.length === 0 ? (
          <p>아직 저장된 영상이 없습니다.</p>
        ) : (
          <ul className={styles.list}>
            {videos.map((video) => (
              <li key={video.id} className={styles.card}>
                <a href={video.url} target="_blank" rel="noopener noreferrer">
                  <Image
                    src={video.thumbnail_url}
                    alt={video.title}
                    width={480}
                    height={360}
                    className={styles.thumbnail}
                  />
                  <p className={styles.title}>{video.title}</p>
                </a>
              </li>
            ))}
          </ul>
        )}
      </main>
    </div>
  );
}
